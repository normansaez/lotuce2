# darc lotuce Project
#	ASI - Andes Scientific Instruments - http://andesscientific.com/
#	Juan Eugenio Venegas Aguilar
#	Diciembre 2015 - Mayo 2016


# ToDo:
#	mostrar ROI
#	mostrar saturacion

# ------------------------------ Imports ------------------------------------- #
import os
import numpy as np
import cv2			# OpenCV
import imutils		# Manages images
#import pyfits		# Manages .fits files
import platform		# See which OS the program is running in
from scipy import ndimage	# For calculating center of mass

import wx			# wxPython is a wrapper of wxWidgets, a GUI generator
from wx.lib import statbmp
from wx.lib.wordwrap import wordwrap
import matplotlib			# For making plots
matplotlib.use('WXAgg')		# The recommended way to use wx with mpl is with the WXAgg backend
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas,  NavigationToolbar2WxAgg as NavigationToolbar

import lotuce_gui_form					# Estructura de la GUI
from lotuce_embedded_data import *		# Archivo de imagenes



# -------------------- Cameras ----------------------------------------------- #

N_CAMS = 4
WIDTH = 200
HEIGHT = 200
SOURCE = "webcam"  # "webcam" o "darc"

class CameraSource_Webcam ( object ):
	def __init__(self, camera=0):
		# Inicializar webcam
		self.capture = cv2.VideoCapture(camera)
		if not self.capture:
			raise Exception("Camera not accessible")

		image = self.get_frames()[0]
		self.saturation = [0.0] * 4
		if image is not None:
			self.shape  = image.shape
			self.height = self.shape[0]
			self.width  = self.shape[1]
		else:
			raise Exception("Camera not accessible")

	def get_frames(self):
		ret, frame = self.capture.read()
		if ret:
			self.saturation = [ np.max(frame) / 255.0 ] * 4
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)	# Entregar en gris para ser compatible con darc
			return [frame, frame, frame, frame]		# Misma imagen repetida
		else:
			return [None, None, None, None]

	def release(self):
		self.capture.release()



class CameraSource_darc ( object ):
	def __init__(self, camera=0):
		# Inicializar darc
		import darc			# Importarlo aca por ahora, para que no sea requisito en modo de prueba con webcams
		self.prefix = 'all'
		self.d_obj = darc.Control(self.prefix)
		self.saturation = [0.0] * 4

		image = self.get_frames()[0]
		if image is not None:
			self.shape  = image.shape
			self.height = self.shape[0]
			self.width  = self.shape[1]
		else:
			raise Exception("Camera not accessible")

	def get_frames(self):
		# Copiado de codigo anterior, revisar
		pxlx = self.d_obj.Get("npxlx")[0]
		pxly = self.d_obj.Get("npxly")[0]
		# print "x: %d" % pxlx;		print "y: %d" % pxly
		stream = self.d_obj.GetStream('%srtcPxlBuf'% self.prefix)
		data = stream[0].reshape( (4*pxly, pxlx) )

		xi_cam0 = 0*pxly
		xf_cam0 = 1*pxly
		yi_cam0 = 0*pxlx
		yf_cam0 = 1*pxlx
		
		xi_cam1 = 1*pxly
		xf_cam1 = 2*pxly
		yi_cam1 = 0*pxlx
		yf_cam1 = 1*pxlx
		
		xi_cam2 = 2*pxly
		xf_cam2 = 3*pxly
		yi_cam2 = 0*pxlx
		yf_cam2 = 1*pxlx
		
		xi_cam3 = 3*pxly
		xf_cam3 = 4*pxly
		yi_cam3 = 0*pxlx
		yf_cam3 = 1*pxlx
		
		# Data per camera
		cam0 = data[xi_cam0:xf_cam0,yi_cam0:yf_cam0]
		cam1 = data[xi_cam1:xf_cam1,yi_cam1:yf_cam1]
		cam2 = data[xi_cam2:xf_cam2,yi_cam2:yf_cam2]
		cam3 = data[xi_cam3:xf_cam3,yi_cam3:yf_cam3]
		
		# Calcular saturacion
		maxi = 2.0**12.0 - 1.0
		self.saturation = [cam0/maxi, cam1/maxi, cam2/maxi, cam3/maxi]
		
		# Entregar en 8 bits para mostrar en GUI
		cam0 = np.array( cam0 / 2**4, dtype=np.uint8 )
		cam1 = np.array( cam1 / 2**4, dtype=np.uint8 )
		cam2 = np.array( cam2 / 2**4, dtype=np.uint8 )
		cam3 = np.array( cam3 / 2**4, dtype=np.uint8 )

		return [cam0, cam1, cam2, cam3]

	def release(self):
		pass



# -------------------- Plots --------------------------------------------------#
import random

class Plots ( object ):
	def __init__( self, panels, sizers, id, cam ):
		self.panels = panels
		self.sizers = sizers
		self.id = id
		self.cam = cam
		self.CM = np.array([0,0])
		
		self.figC = Figure() #tight_layout=True)	# dpi=30, tight_layout=True,   frameon=False
		self.figX = Figure() #tight_layout=True)
		self.figY = Figure() #tight_layout=True)
		
		self.canvasC = FigCanvas(panels[0], -1, self.figC);   self.canvasC.SetMinSize(wx.Size(1,1))
		self.canvasX = FigCanvas(panels[1], -1, self.figX);   self.canvasX.SetMinSize(wx.Size(1,1))
		self.canvasY = FigCanvas(panels[2], -1, self.figY);   self.canvasY.SetMinSize(wx.Size(1,1))

		# Dando este argumento se arregla el problema de tener espacios blancos al borde
		self.axesC = self.figC.add_axes([0., 0., 1., 1.])		#self.figC.add_subplot(111)
		self.axesX = self.figX.add_axes([0., 0., 1., 1.])
		self.axesY = self.figY.add_axes([0., 0., 1., 1.])
		
		sizers[0].Add(self.canvasC, 1, wx.ALL|wx.EXPAND, border=1)
		sizers[1].Add(self.canvasX, 1, wx.ALL|wx.EXPAND, border=1)
		sizers[2].Add(self.canvasY, 1, wx.ALL|wx.EXPAND, border=1)

		x = np.array( range(WIDTH) )
		x_ = x[80:120]
		# self.plot_dataC = self.axesC.scatter([100], [100], s=20)
		self.plot_dataC = self.axesC.plot(x_, x_, "+", mew=10, color=(0, 0, 1),)[0]
		self.plot_dataX = self.axesX.plot(x, x, linewidth=1, color=(0, 0, 1),)[0]
		self.plot_dataY = self.axesY.plot(x, x, linewidth=1, color=(0, 0, 1),)[0]
		self.firstPlot = 0
		
		# self.axesC.set_xbound(lower=80, upper=120); self.axesC.set_ybound(lower=80, upper=120); #self.axesC.grid(True)
		# dev = 5.0;			cent = WIDTH/2.0
		# low = cent-dev;		up = cent+dev
		# print low, " ", up
		# self.axesC.set_xbound(lower=low, upper=up);    self.axesC.set_ybound(lower=low, upper=up);    #self.axesC.grid(True)
		self.axesX.set_xbound(lower=0,   upper=WIDTH); self.axesX.set_ybound(lower=0,   upper=100);   #self.axesX.grid(True)
		self.axesY.set_xbound(lower=0,   upper=100);   self.axesY.set_ybound(lower=0,   upper=WIDTH); #self.axesY.grid(True)
		
		if id in [0, 2]:
			self.axesY.invert_xaxis()
		if id in [2, 3]:
			self.axesX.invert_yaxis()
		self.axesC.invert_yaxis()
		self.axesY.invert_yaxis()
		
		self.axesC.get_xaxis().set_visible(False); self.axesC.get_yaxis().set_visible(False)
		self.axesX.get_xaxis().set_visible(False); self.axesX.get_yaxis().set_visible(False)
		self.axesY.get_xaxis().set_visible(False); self.axesY.get_yaxis().set_visible(False)
		
		# self.axesC.set_axis_off()
		# self.axesX.set_axis_off()
		# self.axesY.set_axis_off()
		
		self.axesC.axis('image')
		self.axesX.axis('image')
		self.axesY.axis('image')
	
		self.canvasC.draw()
		self.canvasX.draw()
		self.canvasY.draw()


	def CalculateProfiles ( self, frame ):
		if self.firstPlot < 1:
			self.background = self.canvasC.copy_from_bbox(self.axesC.bbox)
			self.firstPlot += 1
			for i in range(3):
				self.panels[i].Layout()		# Necesario para re-ajustar la escala
		else:
			x1 = np.array(range(HEIGHT))
			x2 = np.array(range(WIDTH))
			
			y1 = np.array([  frame[:,i].sum() for i in xrange(HEIGHT)  ], dtype=np.double)
			y2 = np.array([  frame[i,:].sum() for i in xrange(WIDTH)  ], dtype=np.double)
			
			y1 = y1 / (y1.max()+1) * 100.0
			y2 = y2 / (y2.max()+1) * 100.0
			
			self.CM = ndimage.measurements.center_of_mass(frame)
			# print CM

			self.figC.suptitle("Sat = " + str(self.cam.saturation[self.id] * 100.0) + "%")
			self.plot_dataC.set_xdata([self.CM[1]]); self.plot_dataC.set_ydata([self.CM[0]]); self.canvasC.draw();  #wx.Yield()
			self.plot_dataX.set_xdata(x1); self.plot_dataX.set_ydata(y1); self.canvasX.draw();  #wx.Yield()
			self.plot_dataY.set_xdata(y2); self.plot_dataY.set_ydata(x2); self.canvasY.draw();  #wx.Yield()

			#self.canvas.restore_region(self.background)
			#self.axes.draw_artist(self.plot_data)
			#self.canvas.blit(self.axes.bbox)
		



# -------------------- LOTUCE GUI ---------------------------------------------#
class LOTUCE_GUI( lotuce_gui_form.LOTUCE_GUI_FORM ):
	def __init__( self, parent ):
		# Initialize frame structure
		lotuce_gui_form.LOTUCE_GUI_FORM.__init__( self, parent )

		# Main window processes key events first
		self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyDown)

		# Set icons
		self.SetIcon(DARKLOTUS.GetIcon())		# Window Icon
		# create here extra tools if needed

		# Init image display
		self.cam = CameraSource_Webcam() if SOURCE == "webcam" else CameraSource_darc() if SOURCE == "darc" else None
		self.InitCameraImages()
		self.ShowVideoStream = True
		self.InitPlots()
		
		# Configure ROI
		self.ROI_sizes = [WIDTH/2] * 4
		self.ROI_positions = [ [WIDTH/2, HEIGHT/2] ] * 4
		
		self.fps = 12		# Estable a este rate
		self.InitTimer()	# Iniciar captura de imagenes
		self.m_panelSettings.SetFocus()



# -------------------- General Functions ------------------------------------- #

	def scale_bitmap(self, bitmap, width, height):
		image = wx.ImageFromBitmap(bitmap)
		image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
		result = wx.BitmapFromImage(image)
		return result


# -------------------- Window Events ----------------------------------------- #

	# On Close window event.
	def OnClose( self, event ):
		self.cam.release()	# Liberar la camara al terminar proceso
		self.timer.Stop()
		event.Skip()

	# On Menu Exit event.
	def OnExit ( self, event ):
		self.Close()
	
	# On Key Down event.
	def OnKeyDown( self, event ):
		if event.GetKeyCode() == wx.WXK_ESCAPE:		# Salir si tecla Escape
			self.Close()
		else:
			event.Skip()

	# Timer used in video streaming mode.
	def InitTimer ( self ):
		self.timer = wx.Timer(self, id=wx.ID_ANY)
		self.Bind(wx.EVT_TIMER, self.NextFrame, id=self.timer.GetId() )
		self.timer.Start(1000.0 / self.fps)


# -------------------- Image Functions --------------------------------------- #

	# Toggle camera stream.
	def StreamToggle ( self, event ):
		self.ShowVideoStream = self.m_checkBoxContExpo.GetValue()

	# Create image display widget.
	def InitCameraImages ( self ):
		self.orig_frames = self.cam.get_frames()
		if self.orig_frames[0] is None:
			print ("Cameras are not connected !")
			return

		self.orig_height, self.orig_width = HEIGHT, WIDTH		#self.orig_frames[0].shape[:2]
		self.bmps = []
		self.ImgControls = []
		self.imagePanels = [self.m_panelImage0, self.m_panelImage1, self.m_panelImage2, self.m_panelImage3]
		self.imageSizers = [self.bSizerImage0, self.bSizerImage1, self.bSizerImage2, self.bSizerImage3]
		
		image = cv2.cvtColor(self.orig_frames[0], cv2.COLOR_GRAY2RGB)
		for i in range(N_CAMS):
			self.bmps.append( wx.BitmapFromBuffer(self.orig_width, self.orig_height, image) )
			self.ImgControls.append( statbmp.GenStaticBitmap(self.imagePanels[i], wx.ID_ANY, self.bmps[i]) )
			self.imageSizers[i].Add(self.ImgControls[i], 0, wx.ALL, 1)

		# Color map options
		self.m_choiceImColor.Append("Gray")
		self.m_choiceImColor.Append("Invert")
		self.m_choiceImColor.AppendItems( filter(lambda x: "COLORMAP" in x, dir(cv2)) )
		self.m_choiceImColor.SetSelection(5)	# Rainbow map = 4L
		self.colorMap = getattr( cv2, filter(lambda x: "COLORMAP" in x, dir(cv2)) [5 - 2] )


	def OnChoiceImColor (self, event ):
		if event.GetSelection() == 0:
			self.colorMap = "gray"
		elif event.GetSelection() == 1:
			self.colorMap = "invert"
		else:
			self.colorMap = getattr( cv2, filter(lambda x: "COLORMAP" in x, dir(cv2)) [event.GetSelection() - 2] )

		if not self.ShowVideoStream:	# Fuerza actualizacion si no hay streaming
			self.ShowFrame(self.orig_frames)


	# Timer event, show next camera frame.
	def NextFrame ( self, event ):
		if self.ShowVideoStream:
			self.orig_frames = self.cam.get_frames()
			if self.orig_frames[0] is None:
				print ("WebCam not connected !")
				return
			self.ShowFrame(self.orig_frames)


	def ShowFrame ( self, frames ):
		show_frames = []

		for i in range(N_CAMS):
			show_frames.append( cv2.resize(frames[i], (HEIGHT,WIDTH)) )		#np.copy(frames[i]) )

			# Graficar perfiles y centroides
			self.plots[i].CalculateProfiles( show_frames[i] )

			# Pasar a 3 canales (para poder mostrar el cursor de color)
			if type(self.colorMap) is long:
				show_frames[i] = cv2.applyColorMap(show_frames[i], self.colorMap)	# Aplicar color map
				show_frames[i] = cv2.cvtColor(show_frames[i], cv2.COLOR_BGR2RGB)	# Pasar de BGR a RGB
			else:
				if self.colorMap == "invert":						# Invertir escala
					show_frames[i] = 255 - show_frames[i]
				show_frames[i] = cv2.cvtColor(show_frames[i], cv2.COLOR_GRAY2RGB)	# Pasar de gris a RGB
				
			# Draw regions of interest and centroid
			CM = np.array(self.plots[i].CM, dtype=np.int16)
			size = self.ROI_sizes[i]
			pos = self.ROI_positions[i]
			pt1 = ( pos[0]-size/2, pos[1]-size/2 )
			pt2 = ( pos[0]+size/2, pos[1]+size/2 )
			cv2.rectangle(show_frames[i], pt1, pt2, (0,255,0), 2 )
			
			pt1 = ( CM[0], 0 )
			pt2 = ( CM[0], HEIGHT )
			pt3 = ( 0, CM[0] )
			pt4 = ( WIDTH, CM[0] )
			cv2.line(show_frames[i], pt1, pt2, (0,0,255), 2 )
			cv2.line(show_frames[i], pt3, pt4, (0,0,255), 2 )
			
			self.bmps[i] = wx.BitmapFromBuffer(self.orig_width, self.orig_height, show_frames[i])
			self.ImgControls[i].SetBitmap(self.bmps[i])


	def OnScrollROI( self, event ):
		idx = self.m_radioBoxCamCalib.GetSelection()
		self.ROI_sizes[idx] = self.m_sliderSize.Value
		self.ROI_positions[idx] = [self.m_sliderPosX.Value, self.m_sliderPosY.Value]
		
		if not self.ShowVideoStream:	# Fuerza actualizacion si no hay streaming
			self.ShowFrame(self.orig_frames)
		
	def OnRadioBoxCamera ( self, event ):
		idx = self.m_radioBoxCamCalib.GetSelection()
		self.m_sliderSize.SetValue(self.ROI_sizes[idx])
		self.m_sliderPosX.SetValue(self.ROI_positions[idx][0])
		self.m_sliderPosY.SetValue(self.ROI_positions[idx][1])
			
# -------------------- Data Analisis Functions ------------------------------- #

	# Create the matplotlib Figure and FigCanvas objects.
	def InitPlots ( self ):
		plotPanels0 = [self.m_panelPlot0C, self.m_panelPlot0X, self.m_panelPlot0Y]
		plotPanels1 = [self.m_panelPlot1C, self.m_panelPlot1X, self.m_panelPlot1Y]
		plotPanels2 = [self.m_panelPlot2C, self.m_panelPlot2X, self.m_panelPlot2Y]
		plotPanels3 = [self.m_panelPlot3C, self.m_panelPlot3X, self.m_panelPlot3Y]	

		plotSizers0 = [self.bSizerPlot0C, self.bSizerPlot0X, self.bSizerPlot0Y]
		plotSizers1 = [self.bSizerPlot1C, self.bSizerPlot1X, self.bSizerPlot1Y]
		plotSizers2 = [self.bSizerPlot2C, self.bSizerPlot2X, self.bSizerPlot2Y]
		plotSizers3 = [self.bSizerPlot3C, self.bSizerPlot3X, self.bSizerPlot3Y]
		
		plots0 = Plots(plotPanels0, plotSizers0, 0, self.cam)
		plots1 = Plots(plotPanels1, plotSizers1, 1, self.cam)
		plots2 = Plots(plotPanels2, plotSizers2, 2, self.cam)
		plots3 = Plots(plotPanels3, plotSizers3, 3, self.cam)
		
		self.plots = [plots0, plots1, plots2, plots3]


	def CalculateProfiles ( self, frames ):
		for i in range(N_CAMS):
			self.plots[i].CalculateProfiles( frames[i] )
		



if __name__ == "__main__":

	app = wx.App(False)
	frame = LOTUCE_GUI(None)
	frame.Show(True)
	app.MainLoop()



# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class LOTUCE_GUI_FORM
###########################################################################

class LOTUCE_GUI_FORM ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"LOTUCE", pos = wx.DefaultPosition, size = wx.Size( 1200,900 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubar1 = wx.MenuBar( 0 )
		self.m_menuFile = wx.Menu()
		self.m_menuItemExit = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"Exit"+ u"\t" + u"Alt+F4", u"Exit program", wx.ITEM_NORMAL )
		self.m_menuFile.AppendItem( self.m_menuItemExit )
		
		self.m_menubar1.Append( self.m_menuFile, u"File" ) 
		
		self.SetMenuBar( self.m_menubar1 )
		
		self.m_statusBar1 = self.CreateStatusBar( 3, wx.ST_SIZEGRIP, wx.ID_ANY )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_splitter1 = wx.SplitterWindow( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3DSASH|wx.SP_LIVE_UPDATE|wx.SP_NO_XP_THEME )
		self.m_splitter1.SetSashGravity( 0 )
		self.m_splitter1.Bind( wx.EVT_IDLE, self.m_splitter1OnIdle )
		
		self.m_panelImagePlots = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panelPlot0C = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerPlot0C = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelPlot0C.SetSizer( self.bSizerPlot0C )
		self.m_panelPlot0C.Layout()
		self.bSizerPlot0C.Fit( self.m_panelPlot0C )
		bSizer8.Add( self.m_panelPlot0C, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panelPlot0X = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerPlot0X = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelPlot0X.SetSizer( self.bSizerPlot0X )
		self.m_panelPlot0X.Layout()
		self.bSizerPlot0X.Fit( self.m_panelPlot0X )
		bSizer8.Add( self.m_panelPlot0X, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panelPlot1X = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerPlot1X = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelPlot1X.SetSizer( self.bSizerPlot1X )
		self.m_panelPlot1X.Layout()
		self.bSizerPlot1X.Fit( self.m_panelPlot1X )
		bSizer8.Add( self.m_panelPlot1X, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panelPlot1C = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerPlot1C = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelPlot1C.SetSizer( self.bSizerPlot1C )
		self.m_panelPlot1C.Layout()
		self.bSizerPlot1C.Fit( self.m_panelPlot1C )
		bSizer8.Add( self.m_panelPlot1C, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		bSizer2.Add( bSizer8, 1, wx.EXPAND, 5 )
		
		bSizer9 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panelPlot0Y = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerPlot0Y = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelPlot0Y.SetSizer( self.bSizerPlot0Y )
		self.m_panelPlot0Y.Layout()
		self.bSizerPlot0Y.Fit( self.m_panelPlot0Y )
		bSizer9.Add( self.m_panelPlot0Y, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panelImage0 = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerImage0 = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelImage0.SetSizer( self.bSizerImage0 )
		self.m_panelImage0.Layout()
		self.bSizerImage0.Fit( self.m_panelImage0 )
		bSizer9.Add( self.m_panelImage0, 1, wx.EXPAND |wx.ALL, 1 )
		
		self.m_panelImage1 = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerImage1 = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelImage1.SetSizer( self.bSizerImage1 )
		self.m_panelImage1.Layout()
		self.bSizerImage1.Fit( self.m_panelImage1 )
		bSizer9.Add( self.m_panelImage1, 1, wx.EXPAND |wx.ALL, 1 )
		
		self.m_panelPlot1Y = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerPlot1Y = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelPlot1Y.SetSizer( self.bSizerPlot1Y )
		self.m_panelPlot1Y.Layout()
		self.bSizerPlot1Y.Fit( self.m_panelPlot1Y )
		bSizer9.Add( self.m_panelPlot1Y, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		bSizer2.Add( bSizer9, 1, wx.EXPAND, 5 )
		
		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panelPlot2Y = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerPlot2Y = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelPlot2Y.SetSizer( self.bSizerPlot2Y )
		self.m_panelPlot2Y.Layout()
		self.bSizerPlot2Y.Fit( self.m_panelPlot2Y )
		bSizer10.Add( self.m_panelPlot2Y, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panelImage2 = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerImage2 = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelImage2.SetSizer( self.bSizerImage2 )
		self.m_panelImage2.Layout()
		self.bSizerImage2.Fit( self.m_panelImage2 )
		bSizer10.Add( self.m_panelImage2, 1, wx.EXPAND |wx.ALL, 1 )
		
		self.m_panelImage3 = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerImage3 = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelImage3.SetSizer( self.bSizerImage3 )
		self.m_panelImage3.Layout()
		self.bSizerImage3.Fit( self.m_panelImage3 )
		bSizer10.Add( self.m_panelImage3, 1, wx.EXPAND |wx.ALL, 1 )
		
		self.m_panelPlot3Y = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerPlot3Y = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelPlot3Y.SetSizer( self.bSizerPlot3Y )
		self.m_panelPlot3Y.Layout()
		self.bSizerPlot3Y.Fit( self.m_panelPlot3Y )
		bSizer10.Add( self.m_panelPlot3Y, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		bSizer2.Add( bSizer10, 1, wx.EXPAND, 5 )
		
		bSizer11 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_panelPlot2C = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerPlot2C = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelPlot2C.SetSizer( self.bSizerPlot2C )
		self.m_panelPlot2C.Layout()
		self.bSizerPlot2C.Fit( self.m_panelPlot2C )
		bSizer11.Add( self.m_panelPlot2C, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panelPlot2X = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerPlot2X = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelPlot2X.SetSizer( self.bSizerPlot2X )
		self.m_panelPlot2X.Layout()
		self.bSizerPlot2X.Fit( self.m_panelPlot2X )
		bSizer11.Add( self.m_panelPlot2X, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panelPlot3X = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerPlot3X = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelPlot3X.SetSizer( self.bSizerPlot3X )
		self.m_panelPlot3X.Layout()
		self.bSizerPlot3X.Fit( self.m_panelPlot3X )
		bSizer11.Add( self.m_panelPlot3X, 1, wx.EXPAND |wx.ALL, 0 )
		
		self.m_panelPlot3C = wx.Panel( self.m_panelImagePlots, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.bSizerPlot3C = wx.BoxSizer( wx.VERTICAL )
		
		
		self.m_panelPlot3C.SetSizer( self.bSizerPlot3C )
		self.m_panelPlot3C.Layout()
		self.bSizerPlot3C.Fit( self.m_panelPlot3C )
		bSizer11.Add( self.m_panelPlot3C, 1, wx.EXPAND |wx.ALL, 0 )
		
		
		bSizer2.Add( bSizer11, 1, wx.EXPAND, 5 )
		
		
		self.m_panelImagePlots.SetSizer( bSizer2 )
		self.m_panelImagePlots.Layout()
		bSizer2.Fit( self.m_panelImagePlots )
		self.m_panel19 = wx.Panel( self.m_splitter1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer39 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook1 = wx.Notebook( self.m_panel19, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panelSettings = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizerSettings = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText21 = wx.StaticText( self.m_panelSettings, wx.ID_ANY, u"  Capture", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )
		self.m_staticText21.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText21.SetForegroundColour( wx.Colour( 40, 60, 210 ) )
		self.m_staticText21.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizerSettings.Add( self.m_staticText21, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer25 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBoxContExpo = wx.CheckBox( self.m_panelSettings, wx.ID_ANY, u"Start / Stop Video Stream", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBoxContExpo.SetValue(True) 
		bSizer25.Add( self.m_checkBoxContExpo, 0, wx.ALL, 5 )
		
		
		bSizerSettings.Add( bSizer25, 0, wx.EXPAND, 5 )
		
		self.m_staticline1 = wx.StaticLine( self.m_panelSettings, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizerSettings.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText211 = wx.StaticText( self.m_panelSettings, wx.ID_ANY, u"  Acquisition", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText211.Wrap( -1 )
		self.m_staticText211.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText211.SetForegroundColour( wx.Colour( 40, 60, 210 ) )
		self.m_staticText211.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizerSettings.Add( self.m_staticText211, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer251 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_checkBox11 = wx.CheckBox( self.m_panelSettings, wx.ID_ANY, u"Start / Stop Remote Acquisition", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox11.SetValue(True) 
		bSizer251.Add( self.m_checkBox11, 0, wx.ALL, 5 )
		
		
		bSizerSettings.Add( bSizer251, 0, wx.EXPAND, 5 )
		
		self.m_staticline11 = wx.StaticLine( self.m_panelSettings, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizerSettings.Add( self.m_staticline11, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText212 = wx.StaticText( self.m_panelSettings, wx.ID_ANY, u"  Calibration of Region of Interest", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText212.Wrap( -1 )
		self.m_staticText212.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText212.SetForegroundColour( wx.Colour( 40, 60, 210 ) )
		self.m_staticText212.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizerSettings.Add( self.m_staticText212, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer29 = wx.BoxSizer( wx.VERTICAL )
		
		m_radioBoxCamCalibChoices = [ u"Cam 0", u"Cam 1", u"Cam 2", u"Cam 3" ]
		self.m_radioBoxCamCalib = wx.RadioBox( self.m_panelSettings, wx.ID_ANY, u"Camera to calibrate", wx.DefaultPosition, wx.DefaultSize, m_radioBoxCamCalibChoices, 1, wx.RA_SPECIFY_ROWS )
		self.m_radioBoxCamCalib.SetSelection( 0 )
		bSizer29.Add( self.m_radioBoxCamCalib, 0, wx.ALL, 5 )
		
		bSizer303 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText123 = wx.StaticText( self.m_panelSettings, wx.ID_ANY, u"Pos X", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText123.Wrap( -1 )
		bSizer303.Add( self.m_staticText123, 0, wx.ALL, 5 )
		
		self.m_sliderPosX = wx.Slider( self.m_panelSettings, wx.ID_ANY, 100, 0, 200, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer303.Add( self.m_sliderPosX, 1, wx.ALL, 5 )
		
		
		bSizer29.Add( bSizer303, 1, wx.EXPAND, 5 )
		
		bSizer302 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText122 = wx.StaticText( self.m_panelSettings, wx.ID_ANY, u"Pos Y", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText122.Wrap( -1 )
		bSizer302.Add( self.m_staticText122, 0, wx.ALL, 5 )
		
		self.m_sliderPosY = wx.Slider( self.m_panelSettings, wx.ID_ANY, 100, 0, 200, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer302.Add( self.m_sliderPosY, 1, wx.ALL, 5 )
		
		
		bSizer29.Add( bSizer302, 1, wx.EXPAND, 5 )
		
		bSizer30 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText12 = wx.StaticText( self.m_panelSettings, wx.ID_ANY, u"Size   ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText12.Wrap( -1 )
		bSizer30.Add( self.m_staticText12, 0, wx.ALL, 5 )
		
		self.m_sliderSize = wx.Slider( self.m_panelSettings, wx.ID_ANY, 100, 0, 200, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL )
		bSizer30.Add( self.m_sliderSize, 1, wx.ALL, 5 )
		
		
		bSizer29.Add( bSizer30, 1, wx.EXPAND, 5 )
		
		
		bSizerSettings.Add( bSizer29, 0, wx.EXPAND, 5 )
		
		self.m_staticline111 = wx.StaticLine( self.m_panelSettings, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizerSettings.Add( self.m_staticline111, 0, wx.EXPAND |wx.ALL, 5 )
		
		self.m_staticText2 = wx.StaticText( self.m_panelSettings, wx.ID_ANY, u"  View", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		self.m_staticText2.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 92, False, wx.EmptyString ) )
		self.m_staticText2.SetForegroundColour( wx.Colour( 40, 60, 210 ) )
		self.m_staticText2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INACTIVECAPTION ) )
		
		bSizerSettings.Add( self.m_staticText2, 0, wx.ALL|wx.EXPAND, 5 )
		
		bSizer241 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText1 = wx.StaticText( self.m_panelSettings, wx.ID_ANY, u"Image Color Map", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		bSizer241.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		m_choiceImColorChoices = []
		self.m_choiceImColor = wx.Choice( self.m_panelSettings, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_choiceImColorChoices, 0 )
		self.m_choiceImColor.SetSelection( 0 )
		bSizer241.Add( self.m_choiceImColor, 1, wx.ALL, 5 )
		
		
		bSizerSettings.Add( bSizer241, 0, wx.EXPAND, 5 )
		
		
		self.m_panelSettings.SetSizer( bSizerSettings )
		self.m_panelSettings.Layout()
		bSizerSettings.Fit( self.m_panelSettings )
		self.m_notebook1.AddPage( self.m_panelSettings, u"Settings", True )
		self.m_panel22 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_notebook1.AddPage( self.m_panel22, u"Covariance Plot", False )
		
		bSizer39.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.m_panel19.SetSizer( bSizer39 )
		self.m_panel19.Layout()
		bSizer39.Fit( self.m_panel19 )
		self.m_splitter1.SplitVertically( self.m_panelImagePlots, self.m_panel19, 800 )
		bSizer3.Add( self.m_splitter1, 1, wx.EXPAND, 1 )
		
		
		self.SetSizer( bSizer3 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.Bind( wx.EVT_MENU, self.OnExit, id = self.m_menuItemExit.GetId() )
		self.m_checkBoxContExpo.Bind( wx.EVT_CHECKBOX, self.StreamToggle )
		self.m_radioBoxCamCalib.Bind( wx.EVT_RADIOBOX, self.OnRadioBoxCamera )
		self.m_sliderPosX.Bind( wx.EVT_SCROLL, self.OnScrollROI )
		self.m_sliderPosY.Bind( wx.EVT_SCROLL, self.OnScrollROI )
		self.m_sliderSize.Bind( wx.EVT_SCROLL, self.OnScrollROI )
		self.m_choiceImColor.Bind( wx.EVT_CHOICE, self.OnChoiceImColor )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnClose( self, event ):
		event.Skip()
	
	def OnExit( self, event ):
		event.Skip()
	
	def StreamToggle( self, event ):
		event.Skip()
	
	def OnRadioBoxCamera( self, event ):
		event.Skip()
	
	def OnScrollROI( self, event ):
		event.Skip()
	
	
	
	def OnChoiceImColor( self, event ):
		event.Skip()
	
	def m_splitter1OnIdle( self, event ):
		self.m_splitter1.SetSashPosition( 800 )
		self.m_splitter1.Unbind( wx.EVT_IDLE )
	


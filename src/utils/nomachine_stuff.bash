COOKIE=`ps -ef | md5sum | cut -f 1 -d " "`
xauth -f ~/Xvfb-0.auth add :1 MIT-MAGIC-COOKIE-1 $COOKIE
xauth add :1 MIT-MAGIC-COOKIE-1 $COOKIE
#Xvfb :1 -auth ~/Xvfb-0.auth -screen 0 1366x768x24 &
Xvfb :1 +extension RANDR -extension XINERAMA -auth ~/Xvfb-0.auth -screen 0 1366x768x24  &
#DISPLAY=:1 nohup /etc/gdm/Xsession xfce4-session &
#DISPLAY=:1 nohup /etc/gdm/Xsession gnome-session &
DISPLAY=:1 nohup gnome-session &

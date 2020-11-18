import os
import sys
import time



os.system("sudo service apache2 stop")
time.sleep(5)
print "apache2 stopped"

os.chdir("/home/pi/node-rtsp-rtmp-server")
os.system("./start_server.sh &")
print "streaming server starting"
time.sleep(40)
print "streaming server started"

os.chdir("/home/pi/picam")
os.system("./picam --alsadev hw:1,0 --rtspout -w 240 -h 160 -v 100000 -f 20 &")

print "Start streaming video"

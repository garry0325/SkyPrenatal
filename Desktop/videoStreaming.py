import os
import sys

width=sys.argv[1]
height=sys.argv[2]
framerate=sys.argv[3]

command="sudo uv4l -nopreview --auto-video_nr --driver raspicam --encoding mjpeg --width {} --height {} --framerate {} --server-option '--port=9090' --server-option '--max-queued-connections=30' --server-option '--max-streams=25' --server-option '--max-threads=29'".format(width,height,framerate)
os.system(command)

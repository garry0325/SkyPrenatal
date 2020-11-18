import os
import sys

width=sys.argv[1]
height=sys.argv[2]
framerate=sys.argv[3]

command="sudo uv4l -nopreview --auto-video_nr --driver raspicam --encoding mjpeg --width %d --height %d --framerate %d --server-option '--port=9090' --server-option '--max-queued-connections=30' --server-option '--max-streams=25' --server-option '--max-threads=29'" %(width,height,framerate)
os.terminal(command)

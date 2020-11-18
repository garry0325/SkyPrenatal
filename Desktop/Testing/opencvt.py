from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

camera=PiCamera()
camera.resolution=(480,320)
camera.framerate=20
rawCapture=PiRGBArray(camera,size=(480,320))

time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture,format="bgr", use_video_port=True):
    image=frame.array
    cv2.imshow("frame",image)
    key=cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)

    if key==ord("q"):
        break

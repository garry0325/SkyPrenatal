import cv2
import numpy as np

cam=cv2.VideoCapture(0)

while True:
    ret, frame=cam.read()
    cv2.imshow('frame',frame)

    if cv2.waitkey(1) & 0xFF==ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


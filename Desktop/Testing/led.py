import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(6,GPIO.OUT)

while True:
    GPIO.output(6,GPIO.HIGH)
    time.sleep(0.6)
    GPIO.output(6,GPIO.LOW)
    time.sleep(0.2)



    

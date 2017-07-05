import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(17, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
print("Starting")
try:
    for x in range(0,50):
        time.sleep(0.1)
        #print(GPIO.input(4))
        print(GPIO.input(17))
except KeyboardInterrupt:
    print("Exit")
    

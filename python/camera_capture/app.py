import time
import gpiodevices
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BOARD)      # use PHYSICAL GPIO Numbering

gpiodevices.setLedGreen(True)
time.sleep(5000)
gpiodevices.setLedYellow(True)
time.sleep(5000)
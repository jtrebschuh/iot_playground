import time
import gpiodevices
import RPi.GPIO as GPIO


gpiodevices.setup()

gpiodevices.setLedGreen(True)
time.sleep(5)
gpiodevices.setLedYellow(True)
time.sleep(5)

gpiodevices.reset()
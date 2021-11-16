import time
import gpiodevices


gpiodevices.setLedGreen(True)
time.sleep(5000)
gpiodevices.setLedYellow(True)
time.sleep(5000)
import time
import gpiodevices
import logging

logging.basicConfig(level=logging.INFO)

gpiodevices.setup()

gpiodevices.setLedGreen(True)
time.sleep(0.5)
gpiodevices.setLedYellow(True)
time.sleep(0.5)

gpiodevices.setLedYellow(False)
gpiodevices.setLedGreen(False)
while True:
    gpiodevices.setLedGreen(gpiodevices.getButtonState())
    time.sleep(0.05)

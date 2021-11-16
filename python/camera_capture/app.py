import time
import gpiodevices
import logging
import iot_camera
from multiprocessing import Process

logging.basicConfig(level=logging.INFO)

gpiodevices.setup()

iot_process = Process(target=iot_camera.main)
iot_process.start()

logging.info("iot_camera started")

gpiodevices.setLedGreen(True)
time.sleep(1)

gpiodevices.setLedYellow(False)
gpiodevices.setLedGreen(False)

while True:
    gpiodevices.setLedGreen(gpiodevices.getButtonState())
    time.sleep(0.05)

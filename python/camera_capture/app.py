import time
import gpiodevices
import logging
import threading
import iot_camera

logging.basicConfig(level=logging.INFO)

gpiodevices.setup()

iot_thread = threading.Thread(target=iot_camera.start_azure_iot())

iot_thread.start()

gpiodevices.setLedGreen(True)
time.sleep(1)

gpiodevices.setLedYellow(False)
gpiodevices.setLedGreen(False)

while True:
    gpiodevices.setLedGreen(gpiodevices.getButtonState())
    time.sleep(0.05)

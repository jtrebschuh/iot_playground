import time
import gpiodevices
import logging
import threading
import iot_camera

logging.basicConfig(level=logging.INFO)

gpiodevices.setup()

gpiodevices.setLedGreen(True)
time.sleep(0.5)
gpiodevices.setLedYellow(True)
time.sleep(0.5)

gpiodevices.setLedYellow(False)
gpiodevices.setLedGreen(False)

iot_camera.start_azure_iot()

#iot_thread = threading.Thread(target=thread_function, args=(1,))

while True:
    gpiodevices.setLedGreen(gpiodevices.getButtonState())
    time.sleep(0.05)

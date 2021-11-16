import time
import gpiodevices
import logging
import threading
import iot_camera
import asyncio

logging.basicConfig(level=logging.INFO)

gpiodevices.setup()

loop = asyncio.get_running_loop()

loop = asyncio.get_running_loop()
user_finished = loop.run_in_executor(None, iot_camera.main)


# iot_process = Process(target=iot_camera.main)
# iot_process.start()

logging.info("iot_camera started")

gpiodevices.setLedGreen(True)
time.sleep(1)

gpiodevices.setLedYellow(False)
gpiodevices.setLedGreen(False)

while True:
    gpiodevices.setLedGreen(gpiodevices.getButtonState())
    time.sleep(0.05)

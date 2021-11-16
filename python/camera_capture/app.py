import time
import gpiodevices
import logging
import iot_camera
from multiprocessing import Process
from dotenv import load_dotenv
from camera_access import capture_and_upload

load_dotenv()

logging.basicConfig(level=logging.INFO)

gpiodevices.setup()

iot_process = iot_camera.IoT_Camera_Thread()
iot_process.start()

logging.info("iot_camera started")

gpiodevices.setLedGreen(True)
time.sleep(1)

gpiodevices.setLedYellow(False)
gpiodevices.setLedGreen(False)

buttonState = False
while True:
    tmp = gpiodevices.getButtonState()
    if not buttonState and tmp:
        capture_and_upload()
    buttonState = tmp 
    time.sleep(0.05)

# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
 
import os, uuid
import asyncio
import threading
import logging
import json
from six.moves import input
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodResponse
from picamera import PiCamera
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from camera_access import capture_and_upload
import gpiodevices


class IoT_Camera_Thread(threading.Thread):

    # overriding constructor
    def __init__(self):
        # calling parent class constructor
        threading.Thread.__init__(self)

    # define your own run method
    def run(self):
        self.loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)

        self.loop.run_until_complete(self.main())
        
    # define behavior for handling methods
    async def method1_listener(device_client):
        while True:
            method_request = await device_client.receive_method_request(
                "p"
            )  # Wait for method1 calls
            logging.info("executed method photo")

            local_file_name = capture_and_upload()

            payload = {"result": True, "data": "execute successfully", "image": local_file_name}  # set response payload
            status = 200  # set return status code

            logging.info("response: "+json.dumps(payload))
            method_response = MethodResponse.create_from_method_request(
                method_request, status, payload
            )
            await device_client.send_method_response(method_response)  # send response

    async def generic_method_listener(device_client):
        while True:
            method_request = (
                await device_client.receive_method_request()
            )  # Wait for unknown method calls
            payload = {"result": False, "data": "unknown method"}  # set response payload
            status = 400  # set return status code
            print("executed unknown method: " + method_request.name)
            method_response = MethodResponse.create_from_method_request(
                method_request, status, payload
            )
            await device_client.send_method_response(method_response)  # send response

    async def main(self):
        
        gpiodevices.setup()
        # The connection string for your device.
        conn_str = os.getenv("AZURE_IOT_CONNECTION_STRING")
        # The client object is used to interact with your Azure IoT hub.
        self.device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)

        # connect the client.
        await self.device_client.connect()

        # define behavior for halting the application
        # def stdin_listener():
        #     while True:
        #         selection = input("Press Q to quit\n")
        #         if selection == "Q" or selection == "q":
        #             print("Quitting...")
        #             break

        # Schedule tasks for Method Listener
        self.listeners = asyncio.gather(
            self.method1_listener(self.device_client),
            self.generic_method_listener(self.device_client)
        )

        # Run the stdin listener in the event loop
        # loop = asyncio.get_running_loop()
        # user_finished = loop.run_in_executor(None, stdin_listener)

        # Wait for user to indicate they are done listening for method calls
        # await user_finished
        

    async def stop(self):
        # Cancel listening
        self.listeners.cancel()
        
        self.loop.close()

        # Finally, disconnect
        await self.device_client.disconnect()

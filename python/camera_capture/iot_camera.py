# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
 
import os, uuid
import asyncio
import threading
from six.moves import input
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import MethodResponse
from dotenv import load_dotenv
from picamera import PiCamera
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__


class IoT_Camera_Thread(threading.Thread):

    # overriding constructor
    def __init__(self):
        # calling parent class constructor
        threading.Thread.__init__(self)

    # define your own run method
    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        loop.run_until_complete(self.main())
        loop.close()
        
    # define behavior for handling methods
    async def method1_listener(self):
        while True:
            method_request = await self.device_client.receive_method_request(
                "p"
            )  # Wait for method1 calls
            print("executed method photo")


            # Retrieve the connection string for use with the application. The storage
            # connection string is stored in an environment variable on the machine
            # running the application called AZURE_STORAGE_CONNECTION_STRING. If the environment variable is
            # created after the application is launched in a console or with Visual Studio,
            # the shell or application needs to be closed and reloaded to take the
            # environment variable into account.
            connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

            # Create the BlobServiceClient object which will be used to create a container client
            blob_service_client = BlobServiceClient.from_connection_string(connect_str)

            # Create a unique name for the container
            container_name = os.getenv('AZURE_STORAGE_CONTAINER_NAME')

            # Create a local directory to hold blob data
            local_path = "./data"
            if not os.path.exists(local_path):
                os.mkdir(local_path)

            # Create a file in the local data directory to upload and download
            local_file_name = str(uuid.uuid4()) + ".jpg"
            upload_file_path = os.path.join(local_path, local_file_name)

            camera = PiCamera()

            camera.capture(upload_file_path)

            # Create a blob client using the local file name as the name for the blob
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)

            print("\nUploading to Azure Storage as blob:\n\t" + local_file_name)

            # Upload the created file
            with open(upload_file_path, "rb") as data:
                blob_client.upload_blob(data)
            print("\nUploaded")
            payload = {"result": True, "data": "execute successfully", "image": local_file_name}  # set response payload
            status = 200  # set return status code

            method_response = MethodResponse.create_from_method_request(
                method_request, status, payload
            )
            
            await self.device_client.send_method_response(method_response)  # send response

    async def generic_method_listener(self):
        while True:
            method_request = (
                await self.device_client.receive_method_request()
            )  # Wait for unknown method calls
            payload = {"result": False, "data": "unknown method"}  # set response payload
            status = 400  # set return status code
            print("executed unknown method: " + method_request.name)
            method_response = MethodResponse.create_from_method_request(
                method_request, status, payload
            )
            await self.device_client.send_method_response(method_response)  # send response
 
    async def main(self):
        
        load_dotenv()

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
            self.method1_listener(),
            self.generic_method_listener(),
        )

        # Run the stdin listener in the event loop
        # loop = asyncio.get_running_loop()
        # user_finished = loop.run_in_executor(None, stdin_listener)

        # Wait for user to indicate they are done listening for method calls
        # await user_finished
        

    async def stop(self):
        # Cancel listening
        self.listeners.cancel()

        # Finally, disconnect
        await self.device_client.disconnect()

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
 
async def main():
    
    load_dotenv()

    # The connection string for your device.
    conn_str = os.getenv("AZURE_IOT_CONNECTION_STRING")
    # The client object is used to interact with your Azure IoT hub.
    device_client = IoTHubDeviceClient.create_from_connection_string(conn_str)
 
    # connect the client.
    await device_client.connect()
 
    # define behavior for handling methods
    async def method1_listener(device_client):
        while True:
            method_request = await device_client.receive_method_request(
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
            print("\Uploaded")
            payload = {"result": True, "data": "execute successfully", "image": local_file_name}  # set response payload
            status = 200  # set return status code

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
 
    # define behavior for halting the application
    def stdin_listener():
        while True:
            selection = input("Press Q to quit\n")
            if selection == "Q" or selection == "q":
                print("Quitting...")
                break
 
    # Schedule tasks for Method Listener
    listeners = asyncio.gather(
        method1_listener(device_client),
        generic_method_listener(device_client),
    )
 
    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)
 
    # Wait for user to indicate they are done listening for method calls
    await user_finished
 
    # Cancel listening
    listeners.cancel()
 
    # Finally, disconnect
    await device_client.disconnect()
 
 
if __name__ == "__main__":
    asyncio.run(main())
 
    # If using Python 3.6 or below, use the following code instead of asyncio.run(main()):
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
# loop.close()
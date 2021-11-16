import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from picamera import PiCamera
from time import sleep
import gpiodevices
import logging
from datetime import datetime


camera = PiCamera()

def capture_and_upload() -> str:
    try:
        logging.info("Capture Camera Image")

        gpiodevices.setLedYellow(True)

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

        now = datetime.now() # current date and time

        # Create a local directory to hold blob data
        local_path = "./"+now.strftime("%Y-%m-%d")
        if not os.path.exists(local_path):
            os.mkdir(local_path)

        # Create a file in the local data directory to upload and download
        local_file_name = now.strftime("%H-%M-%S") + ".jpg"
        upload_file_path = os.path.join(local_path, local_file_name)

        camera.capture(upload_file_path)

        logging.info("Image captured. Start upload")
        gpiodevices.setLedGreen(True)

        # Create a blob client using the local file name as the name for the blob
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)


        # Upload the created file
        with open(upload_file_path, "rb") as data:
            blob_client.upload_blob(data)
        
        logging.info("Uploaded to Azure Storage:" + upload_file_path)
        
        gpiodevices.reset()

        return local_file_name

    except Exception as ex:
        print('Exception:')
        print(ex)
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
from dotenv import load_dotenv
from picamera import PiCamera
from time import sleep

try:
    print("Azure Blob Storage v" + __version__ + " - Python quickstart sample")

    load_dotenv()

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

    camera = PiCamera()

    # Create a local directory to hold blob data
    os.mkdir("./data")
    upload_file_path = F"./data/${str(uuid.uuid4())}.jpg"

    camera.capture(upload_file_path)

    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=upload_file_path)

    print("\nUploading to Azure Storage as blob:\n\t" + upload_file_path)

    # Upload the created file
    with open(upload_file_path, "rb") as data:
        blob_client.upload_blob(data)

except Exception as ex:
    print('Exception:')
    print(ex)
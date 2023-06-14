# General packages, as required
import azure.storage.blob
import uuid
from datetime import datetime, timedelta



# For working with the blob service, at the storage account level
from azure.storage.blob import BlobServiceClient

# For working at the containers, within a storage account
from azure.storage.blob import ContainerClient

# Use the SAS generator function, and SAS permissions class for containers
from azure.storage.blob import ContainerSasPermissions, generate_container_sas

connect_str = "  "
user_container_name = "userimages-id-" + str(uuid.uuid4())[0:4]

# Create the BlobServiceClient object which will be used to create a container client
blob_service_client = BlobServiceClient.from_connection_string(connect_str)
print("**** Client connected to Storage Account: " + blob_service_client.account_name + " ****")

#Create a new container
container_client = blob_service_client.create_container(user_container_name)
print("\nCreated container: " + user_container_name)



# Create a SAS for the container, to be used
print("\nGenerating SAS...")
container_sas = generate_container_sas(blob_service_client.account_name.container_client.container_name,
    container_client.container_name,
    account_key=blob_service_client.credential.account_key,
    permission=ContainerSasPermissions(read=True,write=True,list=True),
    expiry=datetime.utcnow() + timedelta(hours=1),
    start=datetime.utcnow() - timedelta(hours=1)
)

# print the SAS
container_url = "https://" + blob_service_client.account_name + ".blob.core.windows.net/" + container_client.container
full_sas_url = container_url + "?" + container_sas
print("Container SAS for mobile client: ")
print(">> SAS: " + container_sas)
print(">> FULL URL (for web browser): " + full_sas_url + "&comp=list&restype=container")


## MOBILE CLIENT

# For working with blobs, within a container
from azure.storage.blob import BlobClient
import os, pathlib

# Set the image path for upload
current_path = pathlib.Path(__file__).parent.absolute()
image_file_name = "daniel_bundor.jpg"
image_upload_path = os.path.join(current_path, image_file_name)

# Create the blob client for upload
blob_client = BlobClient.from_blob_url(container_url + "/" + image_file_name + "?" + container_sas)
print("Blob Client connected to: " + container_url + "/" + image_file_name + "?" + container_sas)
print("\nUploading blob:\n\t" + image_file_name)

# Upload the created file
with open(image_upload_path, "rb") as data:
    blob_client.upload_blob(data)
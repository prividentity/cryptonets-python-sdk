from cryptonets_python_sdk.factor import FaceFactor

# Initialize API Key and Server URL
api_key = "your_api_key"
server_url = "provided_server_url"

# Image path of the face
image_file_path = "path_to_the_image"

# Initialize the Face Factor object
face_factor = FaceFactor(api_key=api_key, server_url=server_url)

# Call delete from the face factor object
delete_handle = face_factor.delete(uuid="uuid_to_be_deleted")

# Parse enroll result
# See https://docs.private.id/cryptonets-python-sdk/ResultObjects/DeleteResult.html for detailed information
print("Status:{}\nMessage:{}".format(delete_handle.status, delete_handle.message))

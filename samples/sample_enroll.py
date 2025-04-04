from cryptonets_python_sdk.factor import FaceFactor

# Initialize API Key and Server URL
api_key = "your_api_key"
server_url = "provided_server_url"

# Image path of the face
image_file_path = "path_to_the_image"

# Initialize the Face Factor object
face_factor = FaceFactor(api_key=api_key, server_url=server_url)

# Call enroll from the face factor object
result = face_factor.enroll(image_path=image_file_path)

# Parse enroll result
# See https://docs.private.id/cryptonets-python-sdk/ResultObjects/EnrollPredictResult.html for detailed information
print(
    "Status:{}\nFace Validation Message:{}\napi_status:{} \napi_message:{}\nEnroll Level:{}\nPUID:{}\nGUID:{}\nToken:{}\nEnroll_performed:{}".format(
    result.status,
    result.message,
    result.api_status,
    result.api_message,
    result.enroll_level,
    result.puid,
    result.guid,
    result.token,
    result.enroll_performed
    )
)

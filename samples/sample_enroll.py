from cryptonets_python_sdk.factor import FaceFactor

# Initialize API Key and Server URL
api_key = "your_api_key"
server_url = "provided_server_url"

# Image path of the face
image_file_path = "path_to_the_image"

# Initialize the Face Factor object
face_factor = FaceFactor(api_key=api_key, server_url=server_url)

# Call enroll from the face factor object
enroll_handle = face_factor.enroll(image_path=image_file_path)

# Parse enroll result
# See https://docs.private.id/cryptonets-python-sdk/ResultObjects/EnrollPredictResult.html for detailed information
print("Status:{}\nMessage:{}\nEnroll Level:{}\nUUID:{}\nGUID:{}\nToken:{}\n".format(enroll_handle.status,
                                                                                    enroll_handle.message,
                                                                                    enroll_handle.enroll_level,
                                                                                    enroll_handle.uuid,
                                                                                    enroll_handle.guid,
                                                                                    enroll_handle.token))

from cryptonets_python_sdk.factor import FaceFactor

# Initialize API Key and Server URL
api_key = "your_api_key"
server_url = "provided_server_url"

# Image path of the face
image_file_path = "path_to_the_image"

# Initialize the Face Factor object
face_factor = FaceFactor(api_key=api_key, server_url=server_url)

# Call predict from the face factor object
predict_handle = face_factor.predict(image_path=image_file_path)

# Parse enroll result
# See https://docs.private.id/cryptonets-python-sdk/ResultObjects/EnrollPredictResult.html for detailed information
print("Status:{}\nMessage:{}\nEnroll Level:{}\nPUID:{}\nGUID:{}\nToken:{}\n".format(predict_handle.status,
                                                                                    predict_handle.message,
                                                                                    predict_handle.enroll_level,
                                                                                    predict_handle.puid,
                                                                                    predict_handle.guid,
                                                                                    predict_handle.token))

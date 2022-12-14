from cryptonets_python_sdk.factor import FaceFactor

# Initialize API Key and Server URL
api_key = "your_api_key"
server_url = "provided_server_url"

# Image path of the face
image_file_path = "path_to_the_image"

# Initialize the Face Factor object
face_factor = FaceFactor(api_key=api_key, server_url=server_url)

# Call estimate_age from the face factor object
age_handle = face_factor.estimate_age(image_path=image_file_path)

# Error code and Message for the performed operation
print("Error:{}\nMessage:{}".format(age_handle.error, age_handle.message))

# Iterate face objects from the result to see individual results
# See https://docs.private.id/cryptonets-python-sdk/ResultObjects/FaceValidationResult.html for detailed result parsing
for index, face in enumerate(age_handle.face_objects):
    print(
        "Face#:{}\n{}\nReturn Code:{}\nMessage:{}\nAge:{}\nBBox TL:{}\nBBox BR:{}\n".format(index + 1, '-' * 7,
                                                                                            face.return_code,
                                                                                            face.message,
                                                                                            face.age,
                                                                                            face.bounding_box.top_left_coordinate.__str__(),
                                                                                            face.bounding_box.bottom_right_coordinate.__str__()))

# Check if no faces are found in the image
if len(age_handle.face_objects) == 0:
    print("No Faces found!!\n")

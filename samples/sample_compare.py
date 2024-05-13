from cryptonets_python_sdk.factor import FaceFactor

# Initialize API Key and Server URL
api_key = "your_api_key"
server_url = "provided_server_url"

# Image path of the face
image_file_path_1 = "path_to_the_image_1"
image_file_path_2 = "path_to_the_image_2"

# Initialize the Face Factor object
face_factor = FaceFactor(api_key=api_key, server_url=server_url)

# Call compare from the face factor object
compare_handle = face_factor.compare(
    image_path_1=image_file_path_1, image_path_2=image_file_path_2
)

# Iterate face objects from the result to see individual results
# See https://docs.private.id/cryptonets-python-sdk/ResultObjects/CompareResult.html for detailed result parsing
print(
    "Status:{}\nResult:{}\nMessage:{}\nMin:{}\nMean:{}\nMax:{}\n1VR:{}\n2VR:{}\n".format(
        compare_handle.status,
        compare_handle.result,
        compare_handle.message,
        compare_handle.distance_min,
        compare_handle.distance_mean,
        compare_handle.distance_max,
        compare_handle.first_validation_result,
        compare_handle.second_validation_result,
    )
)

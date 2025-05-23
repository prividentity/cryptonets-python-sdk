import pathlib
import sys
from cryptonets_python_sdk.settings.configuration import ConfigObject
from cryptonets_python_sdk.settings.configuration import PARAMETERS
from cryptonets_python_sdk.factor import FaceFactor
from cryptonets_python_sdk.settings.loggingLevel import LoggingLevel
import time

# Initialize images used in the sample methods 
image_file_path = str(pathlib.Path(__file__).parent / "pic.png")
tomhanks_2 = str(pathlib.Path(__file__).parent / "tom_hanks_2.jpg")
compare_face = str(pathlib.Path(__file__).parent / "compare_face1.png")
compare_doc = str(pathlib.Path(__file__).parent / "compare_doc1.png")
face_iso_file = str(pathlib.Path(__file__).parent / "iso_image_1.png")

# Initialize backend parameters variables
server_url = "https://api-xxxxxxxxxxxxxx.cryptonets.com"
api_key = "xxxxxxxxxxxxxxxx"
print_results=True


def create_config_object(collection_name : str ="", relax_face_validation: bool = False):
    """
    Create a configuration object for FaceFactor operations.
    
    This function creates a ConfigObject that can be passed to various FaceFactor methods
    to customize their behavior.
    
    Args:
        collection_name (str): The name of the collection to be added to the configuration.
                               If left empty or not provided the default collection and its
                               embedding model will be used. 
        relax_face_validation (bool): A boolean indicating whether to relax the face validation
                                     requirements for lower quality images.
    
    Returns:
        ConfigObject: A configuration object initialized with the specified parameters.
    """
    config_param = { PARAMETERS.INPUT_IMAGE_FORMAT: "rgb" }
    if collection_name!="":
        config_param[PARAMETERS.COLLECTION_NAME] = collection_name
    if relax_face_validation:
        config_param[PARAMETERS.RELAX_FACE_VALIDATION] = True
    return ConfigObject(config_param)

# Initialize the FaceFactor object
# FaceFactor is the main class that provides access to all biometric operations
# Parameters:
#   - api_key: Your authentication key for the PrivateID API
#   - server_url: The endpoint URL for the PrivateID server
#   - logging_level: Controls the verbosity of logging (LoggingLevel.full provides maximum details)
face_factor = FaceFactor(api_key=api_key,server_url=server_url,logging_level=LoggingLevel.off)

def compare(collection_name=""):
    """
    Compare two face images to determine if they belong to the same person.
    
    This function demonstrates how to use the FaceFactor.compare() method, which provides
    a similarity score between two facial images. Lower distance values indicate higher
    similarity between faces.     
    
    Args:
        collection_name (str): Optional () collection name for grouping related biometric data.
                             If provided, the comparison will be done with the collection embedding
                             model. If left empty or not provided the default collection and its
                             embedding model will be used.
    
    Returns:
        CompareResult: A result object with the following attributes:
            - status: Operation status code (0 indicates success and the comparaison was performed. -1 failure: comparaison was not performed)
            - result: integer indicating if faces match (1) or not (-1) [status is 0 in this case because the comparaison was performed]
            - message: Descriptive message about the operation outcome
            - distance_min/mean/max: Similarity metrics between the faces
            - first/second_validation_result: Validation results for each input image
    """
    start_time = time.time()
    # Image path of the face
    image_file_path_1 = image_file_path
    image_file_path_2 = tomhanks_2

    # Call compare from the face factor object
    result = face_factor.compare(
        image_path_1=image_file_path_1, 
        image_path_2=image_file_path_2,
        config=create_config_object(collection_name)
    )
    end_time = time.time()
    duration = end_time - start_time    
    if print_results:
        print(f"Compare operation took {duration} seconds")
        print(
            "Status:{}\nResult:{}\nMessage:{}\nMin:{}\nMean:{}\nMax:{}\n1VR:{}\n2VR:{}\n".format(
                result.status,
                result.result,
                result.message,
                result.distance_min,
                result.distance_mean,
                result.distance_max,
                result.first_validation_result,
                result.second_validation_result,
            )
        )
    return result

def enroll(collection_name=""):
    """
    Enroll a face into the biometric system.
    
    This function demonstrates how to use the FaceFactor.enroll() method to add a new facial
    biometric profile to the system. Enrollment is required before a face can be recognized
    through the predict operation.
    
    Args:
        collection_name (str): Optional collection name to associate with this enrollment.
                             Collections help organize biometric data into logical groups.
                             If left empty or not provided the default collection and its
                             embedding model will be used.
    
    Returns:
        EnrollPredictResult: A result object with the following attributes:
            - status: Operation status code (0 indicates success)
            - message: Descriptive message about the operation outcome
            - enroll_level: The enrollment quality level achieved
            - puid: Private Unique Identifier assigned to this enrollment
            - guid: Global Unique Identifier for the enrollment
            - token: Authentication token (if applicable)
            - enroll_performed: Boolean indicating if the enrollment was performed
    """
    
    # Call enroll from the face factor object
    start_time = time.time()
    result = face_factor.enroll(image_path=image_file_path,config=create_config_object(collection_name))
    end_time = time.time()
    duration = end_time - start_time
    # Parse enroll result
    if print_results:
        print(f"Enroll operation took {duration} seconds")
        print(f"Result\n{result}")
    return result

def delete(puid:str,collection_name=""):
    """
    Delete a previously enrolled face from the biometric system.
    
    This function demonstrates how to use the FaceFactor.delete() method to remove a specific
    enrollment from the system using its PUID (Private Unique Identifier).
    
    Args:
        puid (str): The Private Unique Identifier of the enrollment to delete.
        collection_name (str): Optional collection name from which to delete the enrollment.
        If left empty or not provided the default collection will be used.
    
    Returns:
        DeleteResult: A result object with the following attributes:
            - status: Operation status code (0 indicates success)
            - message: Descriptive message about the operation outcome
    """
    start_time = time.time()
    # Call delete from the face factor object
    result = face_factor.delete(puid=puid,config_object=create_config_object(collection_name))
    end_time = time.time()
    duration = end_time - start_time
    if print_results: 
        print(f"Delete operation took {duration} seconds")
        print("Status:{}\nMessage:{}".format(result.status, result.message))
    return result

def predict(collection_name=""):
    """
    Match a face against previously enrolled faces in the system.
    
    This function demonstrates how to use the FaceFactor.predict() method to identify if a face
    matches any previously enrolled faces within the specified collection. This is used for
    biometric authentication or identification.
    
    Args:
        collection_name (str): Optional collection name to search within. If provided,
                             the search will be limited to faces in this collection.
                             If left empty or not provided the default collection and its
                             embedding model will be used.
    
    Returns:
        EnrollPredictResult: A result object with the following attributes:
            - status: Operation status code (0 indicates success)
            - message: Descriptive message about the operation outcome
            - enroll_level: The enrollment level of the matched face
            - puid: Private Unique Identifier of the matched enrollment
            - guid: Global Unique Identifier
            - token: Authentication token (if applicable)
            - api_status: API status code, supplmentary information about the status code returned by the rest API call.
            - api_message: API message, supplmentary information about the message returned by the rest API call.
            
    """
    start_time = time.time()
    # Call predict from the face factor object
    result = face_factor.predict(image_path=image_file_path,
                                        config=create_config_object(collection_name))
    end_time = time.time()
    duration = end_time - start_time
    if print_results:
        print(f"Predict operation took {duration} seconds")
        print(f"Result(s)\n{result}")
    return result

def estimate_age():
    """
    Estimate the age of a person from their facial image.
    
    This function demonstrates how to use the FaceFactor.estimate_age() method to analyze
    a face image and determine the approximate age of the detected person(s).
    
    Returns:
        FaceValidationResult: A result object with the following attributes:
            - error: Error code (0 indicates success)
            - message: Descriptive message about the operation outcome
            - face_objects: List of detected faces, each containing:
                - return_code: Face detection status
                - message: Status message
                - age: Estimated age value
                - bounding_box: Face location coordinates in the image
    """
    
    # Call estimate_age from the face factor object
    start_time = time.time()
    result = face_factor.estimate_age(image_path=image_file_path,config=create_config_object())
    end_time = time.time()
    duration = end_time - start_time
        
    if print_results:
        print(f"Estimate age operation took {duration} seconds")
        # Error code and Message for the performed operation
        print("Error:{}\nMessage:{}".format(result.error, result.message))
        # Iterate face objects from the result to see individual results
        for index, face in enumerate(result.face_objects):
            print(
                "Face#:{}\n{}\nReturn Code:{}\nMessage:{}\nAge:{}\nBBox TL:{}\nBBox BR:{}\n".format(
                    index + 1,
                    "-" * 7,
                    face.return_code,
                    face.message,
                    face.age,
                    face.bounding_box.top_left_coordinate.__str__(),
                    face.bounding_box.bottom_right_coordinate.__str__(),
                )
            )

        # Check if no faces are found in the image
        if len(result.face_objects) == 0:
            print("No Faces found!!\n")
    return result

def face_iso():
    """
    Extract an ISO-compliant face image from a larger image.
    
    This function demonstrates how to use the FaceFactor.get_iso_face() method to detect
    and extract a standardized face image suitable for facial recognition processing.
    The output follows ISO/IEC 19794-5 specifications for face image data.
    
    Returns:
        IsoFaceResult: A result object with the following attributes:
            - status: Operation status code (0 indicates success)
            - message: Descriptive message about the operation outcome
            - iso_image_width/height/channels: Dimensions of the extracted face image
            - confidence: Confidence score of the face detection
            - image: The extracted ISO-compliant face image
    """
    
    start_time = time.time()
    # Call get_iso_face from the face factor object
    result = face_factor.get_iso_face(image_path = face_iso_file)
    end_time = time.time()
    duration = end_time - start_time    
    if print_results:
        print(f"Face ISO operation took {duration} seconds")
        print(
            "Status:{}\nMessage:{}\nIso Image Width:{}\nIso Image Height:{}\nIso Image Channels:{}\nConfidence:{}\nImage:{}\n".format(
                result.status,
                result.message,
                result.iso_image_width,
                result.iso_image_height,
                result.iso_image_channels,
                result.confidence,
                result.image
            )
        )
    return result

def compare_doc_with_face(collection_name=""):
    """
    Compare a face image with a face in an identity document image.
    
    This function demonstrates how to use the FaceFactor.compare_doc_with_face() method to verify
    if a person's photo matches the face in their identity document (e.g., passport, driver's license).
    This is useful for document verification workflows.
    
    Args:
        collection_name (str): Optional collection name to associate with this operation.
        If left empty or not provided the default collection and its
        embedding model will be used.
    
    Returns:
        CompareResult: A comparison result object with the following attributes:
            - status: Operation status code (0 indicates success and the comparaison was performed. -1 failure: comparaison was not performed)
            - result: integer indicating if faces match (1) or not (-1) [status is 0 in this case because the comparaison was performed]
            - message: Descriptive message about the operation outcome
            - distance_min/mean/max: Similarity metrics between the faces
            - first/second_validation_result: Validation results for each image
    """
    start_time = time.time()
    # Perform 1:1 verification between a face image and a document image
    result = face_factor.compare_doc_with_face(
        face_path=compare_face,   # Path to the portrait image
        doc_path=compare_doc,       # Path to the document (e.g., driver's license) image
        config=create_config_object(collection_name)
    )
    end_time = time.time()
    duration = end_time - start_time
    if print_results:
        print(f"compare_doc_with_face operation took {duration} seconds")
        print(
            "Status:{}\nMessage:{}\nDistance:{}\nFirst Validation:{}\nSecond Validation:{}\n".format(
                result.status,
                result.message,
                result.distance_min,
                result.first_validation_result,
                result.second_validation_result,
            )
        )
    return result

def validate():
    """
    Validate if an image contains a recognizable face suitable for biometric operations.
    
    This function demonstrates how to use the FaceFactor.is_valid() method to check if an
    image contains a valid face that meets quality requirements for facial recognition.
    This helps prevent errors in subsequent operations like enrollment or matching.
    
    Returns:
        FaceValidationResult: A result object with the following attributes:
            - error: Error code (0 indicates success)
            - message: Descriptive message about the operation outcome
            - face_objects: List of detected faces with properties including:
                - return_code: Face detection status
                - message: Status message
                - bounding_box: Facial bounding box coordinates
    """
    # Call is_valid from the face factor object
    start_time = time.time()
    result = face_factor.is_valid(image_path=image_file_path)
    end_time = time.time()
    duration = end_time - start_time
    if print_results:
        print(f"Validate operation took {duration} seconds")
        # Error code and Message for the performed operation
        print("Error:{}\nMessage:{}".format(result.error, result.message))
        if print_results:
            for index, face in enumerate(result.face_objects):
                print(
                    "Face#:{}\n{}\nReturn Code:{}\nMessage:{}\nBBox TL:{}\nBBox BR:{}\n".format(
                        index + 1,
                        "-" * 7,
                        face.return_code,
                        face.message,
                        face.bounding_box.top_left_coordinate.__str__(),
                        face.bounding_box.bottom_right_coordinate.__str__(),
                    )
                )

        # Check if no faces are found in the image
        if len(result.face_objects) == 0:
            print("No Faces found!!\n")

def detect_spoof():
    """
    Check if a facial image is a spoof attempt (e.g., photo of a photo, mask, screen).
    
    This function demonstrates how to use the FaceFactor.antispoof_check() method to
    detect potential spoofing attempts in facial biometric systems. This adds an extra
    layer of security to prevent presentation attacks.
    
    Returns:
        AntispoofCheckResult: A result object with the following attributes:
            - status: Operation status code (0 indicates success)
            - message: Descriptive message about the operation outcome
            - is_spoof: Boolean indicating if the image is detected as a spoof attempt
    """
    start_time = time.time()
    result = face_factor.antispoof_check(image_path=spoof_file)
    end_time = time.time()
    duration = end_time - start_time
    if print_results:
        print(f"Detect Spoof operation took {duration} seconds")
        print("Status:{}\nMessage:{}\nIs Spoof:{}".format(result.status, result.message,result.is_spoof))
    return result

def enroll_predict_delete(collection_name=""):
    """
    Demonstrate a complete biometric workflow: enroll, predict, and delete.
    
    This function shows a typical usage pattern of the FaceFactor SDK by:
    1. Enrolling a face in the system
    2. Verifying the face can be correctly identified
    3. Cleaning up by removing the enrollment from the system
    
    This represents a complete lifecycle test of the biometric system.
    
    Args:
        collection_name (str): Optional collection name to use for this workflow.
        If left empty or not provided the default collection and its
        embedding model will be used.
    
    Returns:
        int: 1 if the workflow completed successfully, 0 if any step failed.
    """
    enroll_result = enroll(collection_name)
    if (enroll_result.puid==""):
        return 0
    predict_result = predict(collection_name)
    if (enroll_result.puid != predict_result.puid):
        return  0
    delete_result = delete(enroll_result.puid, collection_name)
    if (delete_result.status!=0):
            return 0
    return 1

def basic_enroll_predict_delete():
    """
    Run the enroll-predict-delete workflow across multiple collections.
    
    This function tests the core biometric workflow (enroll, predict, delete)
    across different collections to verify system functionality across different
    configuration settings. It serves as both a system test and a usage example.
    
    Collections tested:
        - Default (no specific collection)
        - RES100 (resolution configuration 100)
        - RES200 (resolution configuration 200)
    
    Returns:
        int: 1 upon completion, with console output indicating success rate.
    """
    i =0
    i+=enroll_predict_delete()
    i+=enroll_predict_delete("RES100")
    i+=enroll_predict_delete("RES200")
    print(f'Passed {i} out of 3')
    return 1

if __name__ == "__main__":
    basic_enroll_predict_delete()


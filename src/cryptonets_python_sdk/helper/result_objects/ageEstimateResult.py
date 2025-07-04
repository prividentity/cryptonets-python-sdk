from typing import List

from cryptonets_python_sdk.settings.configuration import ANTISPOOFING_STATUSES
from ..utils import FaceValidationCode, BoundingBox , Point
from ..messages import Message
from .callStatus import CallStatus,ApiReturnStatus


class FaceTraitObject:
    """Face Trait Object class encapsulate a face trait image which has a validation code and message associated with it.
    """
    def __init__(self, validation_code:FaceValidationCode=FaceValidationCode.InvalidImage, message=None):
        """Face Trait Object constructor.
        """
        if (not isinstance(validation_code, FaceValidationCode)):
            raise TypeError("validation_code must be an instance of FaceValidationCode Enum")       
        
        self._validation_code = validation_code
        if message == None:
            self._message = Message().get_message(self.validation_code, prompting_message=False)    
        else:
            if (not isinstance(message, str)):
                raise TypeError("message must be a string")
            else:
                self._message = message
    @property
    def validation_code(self) -> FaceValidationCode:
        """Get the validation code."""
        return self._validation_code
    @validation_code.setter
    def validation_code(self, value:FaceValidationCode):
        """Set the validation code."""
        if (not isinstance(value, FaceValidationCode)):
            raise TypeError("validation_code must be an instance of FaceValidationCode Enum")
        self._validation_code = value

    @property
    def message(self) -> str:
        """Get the message."""
        return self._message
    @message.setter
    def message(self, value:str):
        """Set the message."""
        if (not isinstance(value, str)):
            raise TypeError("message must be a string")
        self._message = value


class FaceAgeObjectResult():
    """Face Age Object Result class encapsulates the age estimation results of a face.
    It includes the predicted age, age confidence score, face confidence score, bounding box, and a list of face traits.
    """
    def __init__(
        self,
        face_traits=None,
        message=None,
        age:float=None,   
        antispoofing_status: ANTISPOOFING_STATUSES = None,
        age_confidence_score:float=None,
        bounding_box:BoundingBox=None,
        face_confidence_score:float=None
    ):
        """Face Age Object Result class for handling the age estimation results of a face.
        """

        if face_traits == None :
            self._face_traits = []
        elif isinstance(face_traits, FaceTraitObject):
            self._face_traits = [face_traits]
        elif isinstance(face_traits, list):
            self._face_traits = face_traits
        else:
            raise TypeError("face_traits must be an instance of FaceTraitObject or a list of FaceTraitObject")       

        if message == None:
            self._message = ""            
        elif isinstance(message, str):
            self._message = message
        else:
            raise TypeError("message must be a string")

        if bounding_box is None:
            self._bounding_box = BoundingBox()
        elif isinstance(bounding_box, BoundingBox):
            self._bounding_box = bounding_box
        else:
            raise TypeError("bounding_box must be an instance of BoundingBox")
        
        if age is None:
            self._age = 0.0
        elif isinstance(age, (int, float)):
            self._age = float(age)
        else:
            raise TypeError("age must be a float or int")   
        
        if age_confidence_score is None:
            self._age_confidence_score = 0.0
        elif isinstance(age_confidence_score, (int, float)):
            self._age_confidence_score = float(age_confidence_score)
        else:
            raise TypeError("age_confidence_score must be a float or int")

        if face_confidence_score is None:
            self._face_confidence_score = 0.0
        elif isinstance(face_confidence_score, (int, float)):
            self._face_confidence_score = float(face_confidence_score)
        else:
            raise TypeError("face_confidence_score must be a float or int")
        
        if antispoofing_status is None:
            self._antispoofing_status = ANTISPOOFING_STATUSES.AS_NOT_PERFORMED
        elif isinstance(antispoofing_status, ANTISPOOFING_STATUSES):
            self._antispoofing_status = antispoofing_status
        else:
            raise TypeError("antispoofing_status must be an instance of ANTISPOOFING_STATUSES Enum")

    @property
    def age(self):
        """Get the predicted age."""
        return self._age

    @age.setter
    def age(self, value):
        """Set the predicted age."""
        self._age = value

    @property
    def age_confidence_score(self)-> float:
        """Get the age confidence score."""
        return self._age_confidence_score

    @age_confidence_score.setter
    def age_confidence_score(self, value):
        """Set the age confidence score."""
        self._age_confidence_score = value

    @property
    def face_confidence_score(self) -> float:
        """Get the face confidence score."""
        return self._face_confidence_score

    @face_confidence_score.setter
    def face_confidence_score(self, value):
        """Set the face confidence score."""
        self._face_confidence_score = value

    @property
    def bounding_box(self) -> BoundingBox:
        """Get the bounding box."""
        return self._bounding_box

    @bounding_box.setter
    def bounding_box(self, value):
        """Set the bounding box."""
        self._bounding_box = value

    @property
    def face_traits(self) -> List[FaceTraitObject]:
        """Get the list of face traits."""
        return self._face_traits

    def add_face_trait(self, trait):
        """Add a trait to the face_traits list."""
        self._face_traits.append(trait)

    @property
    def antispoofing_status(self) -> ANTISPOOFING_STATUSES:
        """Get the antispoofing status."""
        return self._antispoofing_status

    @antispoofing_status.setter
    def antispoofing_status(self, value: ANTISPOOFING_STATUSES):
        """Set the antispoofing status."""
        if not isinstance(value, ANTISPOOFING_STATUSES):
            raise TypeError("antispoofing_status must be an instance of ANTISPOOFING_STATUSES Enum")
        self._antispoofing_status = value

class AgeEstimateResult:
    """Age Estimation result class is used to encapsulate the results of the FaceFactory's age estimation operation: 
    FaceFactory.estimate_age
    It includes the operation status code, message, and a list of FaceAgeObjectResult.
    - operation_status_code: if equal to ApiReturnStatus.API_NO_ERROR (0), it indicate that the operation is successful.
    and face_age_objects will contain the list of detected faces with their estimated ages.
    If the operation failed, operation_status_code will contain the error code and operation_message will contain
    the error message explaining the error. 
    In cas eof error , face_age_objects will be None.    
    The operation is considered successful if no face were detected in the image.
    In his case face_age_objects will be an empty list.
    - operation_message: will be set to an empty string if the operation is successful. If the operation failed, it will contain the error message explaining the error.
    - face_age_objects: A list of the detected faces with their estimated ages.
    Each FaceAgeObjectResult contains the following attributes:
    - face_traits: A list of FaceTraitObject, each containing a validation code (FaceValidationCode) and a message (non prompting style).
    - bounding_box: A BoundingBox object representing the bounding box of the face.
    - face_confidence_score: A float representing the confidence score of the face detection.
    - age_confidence_score: A float representing the confidence score of the age estimation.
    - antispoofing_status: A string representing the antispoofing status of the face. See ANTISPOOFING_STATUSES for possible values. 
    The antispoof pass is not enabled by default. You need to set the configuration parameter DISABLE_AGE_ESTIMATION_ANTISPOOF to False to enable it.
    - age: A float representing the estimated age of the face. If age is not estimated or the face is not valid or not detected, it will be set to -1.0.
    """
    def __init__(self, operation_status_code:ApiReturnStatus=ApiReturnStatus.API_GENERIC_ERROR, operation_message:str=""):
        """Age Estimation result class for handling the detected faces and their estimated ages. 
        """
        if not isinstance(operation_status_code, ApiReturnStatus):
            raise TypeError("operation_status_code must be an instance of ApiReturnStatus Enum")
        if not isinstance(operation_message, str):
            raise TypeError("operation_message must be a string")
        self._operation_status_code = operation_status_code
        self._operation_message = operation_message
        self._face_age_objects = []

    @property
    def operation_status_code(self) -> ApiReturnStatus:
        """
        Returns the status of the operation
        """
        return self._operation_status_code
    
    @operation_status_code.setter
    def operation_status_code(self, value):
        """
        Set the operation_status_code of the operation
        """
        if not isinstance(value, ApiReturnStatus):
            raise TypeError("operation_status_code must be an instance of ApiReturnStatus Enum")
        self._operation_status_code = value

    @property
    def operation_message(self) -> str:
        """
        Returns the message of the operation
        """
        return self._operation_message

    @property
    def face_age_objects(self) -> List[FaceAgeObjectResult]:
        """
        Returns the list of Face Age Objects
        """
        return self._face_age_objects

    def append_face_age_objects(self,item:FaceAgeObjectResult):
        """
        Append a FaceAgeObjectResult to the list of face objects.
        """
        if not isinstance(item, FaceAgeObjectResult):
            raise TypeError("item must be an instance of FaceAgeObjectResult")
        self._face_age_objects.append(item)

    @operation_message.setter
    def operation_message(self, value):
        """
        Set the operation_message of the operation
        """
        if not isinstance(value, str):
            raise TypeError("operation_message must be a string")
        self._operation_message = value

    @face_age_objects.setter
    def face_age_objects(self, value):
        """
        Set the list of face objects.
        """
        if not isinstance(value, list):
            raise TypeError("value must be a list of FaceAgeObjectResult")
        for item in value:
            if not isinstance(item, FaceAgeObjectResult):
                raise TypeError("item must be an instance of FaceAgeObjectResult")
        if not value:
            value = []
        if not all(isinstance(item, FaceAgeObjectResult) for item in value):
            raise TypeError("All items in value must be instances of FaceAgeObjectResult")
        self._face_age_objects = value

    @staticmethod
    def from_json(data):
        """
        Create an AgeEstimateResult from a JSON-like dictionary.
        """
        result = AgeEstimateResult()
        try:
            if not isinstance(data, dict):
                raise TypeError("data must be a dictionary")
            
            if 'call_status' not in data or 'ages' not in data:
                raise ValueError("data must contain 'call_status' and 'ages' keys")
            
            call_status = CallStatus.from_dict(data['call_status'])  
            returned_code = ApiReturnStatus(call_status.return_status)
            # Call failed, set the operation status code and message
            if returned_code != ApiReturnStatus.API_NO_ERROR:
                result.operation_status_code = returned_code
                result.operation_message = call_status.return_message
                result._face_age_objects = []
                return
            else:
                result.operation_status_code = ApiReturnStatus.API_NO_ERROR
                result.operation_message = ""
                
            # should not happen, so raising an errir 
            if not isinstance(data['ages'], dict) or 'ages' not in data['ages']:
                raise ValueError("data['ages'] must be a dictionary with 'ages' key")
            if not isinstance(data['ages']['ages'], list):
                raise ValueError("data['ages']['ages'] must be a list")
            
            ages_list = []
            for age in data['ages']['ages']:               
                bbox = BoundingBox(age['bounding_box']['top_left'],age['bounding_box']['bottom_right'])                
                face_trait_with_message =[]
                message_api = Message()
                for trait in age.get('face_traits', []):
                    face_trait_with_message.append(
                        FaceTraitObject(
                            validation_code=FaceValidationCode(trait),
                            message=message_api.get_message(code = trait, prompting_message=False)
                        )
                    )
                ages_list.append(
                    FaceAgeObjectResult(
                        face_traits=face_trait_with_message,
                        bounding_box=bbox,
                        face_confidence_score=age['face_confidence_score'],
                        antispoofing_status = ANTISPOOFING_STATUSES(age['antispoofing_status']),                  
                        age_confidence_score=age['age_confidence_score'],
                        age=age['estimated_age']
                    )
                )
            result.face_age_objects = ages_list
        except Exception as e:
            result.operation_status_code =  ApiReturnStatus.API_UNHANDLED_EXCEPTION.value
            result.operation_message = f"Error parsing AgeEstimateResult: {str(e)}"
        return result
    
    @staticmethod
    def print(age_estimate_result):
        """
        Print a human-readable representation of an AgeEstimateResult instance.
        
        Parameters:
        -----------
        age_estimate_result : AgeEstimateResult
            The AgeEstimateResult instance to display
        
        Returns:
        --------
        AgeEstimateResult
            The input instance (for method chaining)
        """
        if not isinstance(age_estimate_result, AgeEstimateResult):
            raise TypeError("age_estimate_result must be an instance of AgeEstimateResult")
        
        print(f"Operation Status Code: {age_estimate_result.operation_status_code.name}")
        print(f"Message: {age_estimate_result.operation_message}")
        
        face_objects = age_estimate_result.face_age_objects
        if face_objects:
            print(f"\nNumber of detected faces: {len(face_objects)}")
            
            for i, face in enumerate(face_objects):
                print(f"\nFace #{i+1}:")
                print(f"  Estimated Age: {face.age}")
                print(f"  Age Confidence Score: {face.age_confidence_score}")
                print(f"  Face Confidence Score: {face.face_confidence_score}")
                print(f"  Antispoofing Status: {face.antispoofing_status.name}")
                print(f"  Bounding Box: {face.bounding_box}")
                
                if face.face_traits:
                    print(f"  Face Traits:")
                    for j, trait in enumerate(face.face_traits):
                        print(f"    Trait #{j+1}:")
                        print(f"      Validation Code(Name: {trait.validation_code}, code: {trait.validation_code.value})")
                        print(f"      Message: {trait.message}")
        else:
            print("\nNo faces detected.")

        return age_estimate_result  # Return the instance for method chaining
        
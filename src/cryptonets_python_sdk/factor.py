"""Factor implements the functionalities of each factors to generate and verify Private IDs .
"""
import os
import pathlib
import platform
import sys
import traceback
from typing import Union, List
import numpy as np

from .factor_modules.FaceModule import Face
from .helper.decorators import Singleton
from .helper.messages import Message
from .helper.result_objects.compareResult import FaceCompareResult
from .helper.result_objects.deleteResult import FaceDeleteResult
from .helper.result_objects.enrollPredictResult import FaceEnrollPredictResult
from .helper.result_objects.faceValidationResult import FaceValidationResult
from .helper.result_objects.antispoofCheckResult import AntispoofCheckResult
from .helper.result_objects.ageEstimateResult import AgeEstimateResult
from .helper.result_objects.isoFaceResult import ISOFaceResult
from .helper.utils import image_path_to_array
from .settings.configuration import ConfigObject, PARAMETERS
from .settings.loggingLevel import LoggingLevel
from .settings.supportedPlatforms import SupportedPlatforms


class FaceFactor(metaclass=Singleton):
    """The FaceFactor class implements the following methods :

        1. is_valid: Verifies the face of the user.
        2. estimate_age: Predicts the age of the face.
        3. compare: Compare two faces for verification.
        4. enroll: Enrolls the face of the user.
        5. predict: Predicts the face of the user.
        6. delete: Deletes the user from the system
        7. antispoof_check: Check if the image is spoofed or not
        8. get_iso_face: Takes the face image and gives back the image in ISO Spec format
        9. compare_doc_with_face: Check if the images are of same person or not

        Parameters
        ----------
        api_key : str
            The API key for using the FaceFactor server.

        server_url : str
            The URL of the FaceFactor server.

        logging_level : LoggingLevel (Optional)
            LoggingLevel needed while performing operation

        config : ConfigObject (Optional)
            Configuration class object with parameters

        Returns
        -------
        FaceFactor
            Instance of the FaceFactor class.

        Methods
        -------
        is_valid
        estimate_age
        compare
        enroll
        predict
        delete
        antispoof_check
        get_iso_face
        compare_doc_with_face
    """

    def __init__(
        self,
        api_key: str = None,
        server_url: str = None,
        logging_level: LoggingLevel = LoggingLevel.off,        
        config: ConfigObject = None,
    ):

        try:
            if platform.system() not in SupportedPlatforms.supportedOS.value:
                raise OSError("Invalid OS")
            if server_url is None and (
                os.environ.get("PI_SERVER_URL") is None
                or len(os.environ.get("PI_SERVER_URL")) <= 0
            ):
                raise ValueError("Server URL has to be configured")
            if api_key is None and (
                os.environ.get("PI_API_KEY") is None
                or len(os.environ.get("PI_API_KEY")) <= 0
            ):
                raise ValueError("API Key is required.")
            
            if server_url is None:
                self._server_url = os.environ.get("PI_SERVER_URL")
            else:
                self._server_url = server_url
            if api_key is None:
                self._api_key = os.environ.get("PI_API_KEY")
            else:
                self._api_key = api_key
            
            if self._server_url[-1] == "/":
                self._server_url = self._server_url[:-1]

            self._config_object = config
            self._logging_level = logging_level            
            self.face_factor = Face(
                api_key=self._api_key,
                server_url=self._server_url,
                logging_level=self._logging_level,                
                config_object=self._config_object,
            )
            self.message = Message()
        except ValueError as exp:
            print("Initialization Failed: {}\n".format(exp))
            print(
                "Please refer to the usage documentation for setting up "
                "Factor:: \nhttps://docs.private.id/cryptonets-python-sdk/usage.html"
            )
            sys.exit(1)
        except OSError as exp:
            print("Initialization Failed: {}\n".format(exp))
            print(
                "Please refer to the usage documentation for setting up "
                "Factor:: \nhttps://docs.private.id/cryptonets-python-sdk/usage.html"
            )
            sys.exit(1)

    def update_config(self, config):
        self.face_factor.update_config(config_object=config)

    def is_valid(
        self,
        image_path: str = None,
        image_data: np.array = None,
        config: ConfigObject = None,
    ) -> FaceValidationResult:
        """Check if the image is valid for using in the face recognition

        Parameters
        ----------
        image_path
            Directory path to the image file

        config (Optional)
            Additional configuration parameters for the operation

        image_data (Optional)
            Image data in numpy RGB format

        Returns
        -------
        FaceValidationResult
            error: int [0 if successful -1 if any error]

            message: str [Message from the operation]

            face_objects: List[FaceObjectResult]

        """
        try:
            if (
                config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in config.config_param
            ):
                input_format = config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            elif (
                self.config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in self.config.config_param
            ):
                input_format = self.config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            else:
                input_format = "rgb"
            if (image_path is not None and image_data is not None) or (
                image_path is None and image_data is None
            ):
                return FaceValidationResult(
                    message="Specify either image_path or image_data"
                )
            img_data = None
            if image_data is not None:
                if not isinstance(image_data, np.ndarray):
                    return FaceValidationResult(
                        message="Required numpy array in RGB/RGBA/BGR format"
                    )
                img_data = image_data
            if image_path is not None and len(image_path) > 0:
                if not os.path.exists(image_path):
                    return FaceValidationResult(message=self.message.get_message(101))
                img_data = image_path_to_array(image_path, input_format=input_format)
            if img_data is None:
                return FaceValidationResult(message=self.message.IS_VALID_ERROR)

            # Check image dimensions
            if img_data.shape[0] <= 224 or img_data.shape[1] <= 224:
                return FaceValidationResult(
                    message="Image dimensions should be greater than 224x224."
                )

            return self.face_factor.is_valid(image_data=img_data, config_object=config)
        except Exception as e:
            print("Oops: {}\nTrace: {}".format(e, traceback.format_exc()))
            print(
                "Issue Tracker:: \nhttps://github.com/prividentity/cryptonets-python-sdk/issues"
            )
            return FaceValidationResult(message=self.message.IS_VALID_ERROR)

    def estimate_age(
        self,
        image_path: str = None,
        image_data: np.array = None,
        config: ConfigObject = None,
    ) -> AgeEstimateResult:
        """Check if the image is valid and returns the age of the image

        Parameters
        ----------
        image_path
            Directory path to the image file

        config (Optional)
            Additional configuration parameters for the operation

        image_data (Optional)
            Image data in numpy RGB format

        Returns
        -------
        AgeEstimateResult
            operation_status_code: ApiReturnStatus [ApiReturnStatus.API_NO_ERROR (0) if successful, failure otherwise].
                                   if failure, face_age_objects list will be None. 
                                   The operation is considered successful if no face were detected in the image.
                                   In his case face_age_objects will be an empty list.
            operation_message: str [Message explaining the error  if any]
            face_age_objects: List[FaceAgeObjectResult] 
        """
        try:
            if (
                config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in config.config_param
            ):
                input_format = config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            elif (
                self.config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in self.config.config_param
            ):
                input_format = self.config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            else:
                input_format = "rgb"
            if (image_path is not None and image_data is not None) or (
                image_path is None and image_data is None
            ):
                return AgeEstimateResult(
                    message="Specify either image_path or image_data"
                )
            img_data = None
            if image_data is not None:
                if not isinstance(image_data, np.ndarray):
                    return AgeEstimateResult(
                        message="Required numpy array in RGB/RGBA/BGR format"
                    )
                img_data = image_data
            if image_path is not None and len(image_path) > 0:
                if not os.path.exists(image_path):
                    return AgeEstimateResult(message=self.message.get_message(101))
                img_data = image_path_to_array(image_path, input_format=input_format)
            if img_data is None:
                return AgeEstimateResult(message=self.message.AGE_ESTIMATE_ERROR)

            # Check image dimensions
            if img_data.shape[0] <= 224 or img_data.shape[1] <= 224:
                return AgeEstimateResult(
                    message="Image dimensions should be greater than 224x224."
                )

            return self.face_factor.estimate_age(
                image_data=img_data, config_object=config
            )
        except Exception as e:
            print("Oops: {}\nTrace: {}".format(e, traceback.format_exc()))
            print(
                "Issue Tracker:: \nhttps://github.com/prividentity/cryptonets-python-sdk/issues"
            )
            return AgeEstimateResult(message=self.message.AGE_ESTIMATE_ERROR)

    def enroll(
        self,
        image_path: str = None,
        image_data: np.array = None,
        config: ConfigObject = None,
    ) -> FaceEnrollPredictResult:
        """Enrolls the image in the face recognition server

        Parameters
        ----------
        image_path
            Directory path to the image file

        config (Optional)
            Additional configuration parameters for the operation

        image_data (Optional)
            Image data in numpy RGB format

        Returns
        -------
        FaceEnrollPredictResult

        """

        try:
            if (
                config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in config.config_param
            ):
                input_format = config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            elif (
                self.config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in self.config.config_param
            ):
                input_format = self.config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            else:
                input_format = "rgb"
            if (image_path is not None and image_data is not None) or (
                image_path is None and image_data is None
            ):
                return FaceEnrollPredictResult(
                    message="Specify either image_path or image_data"
                )
            img_data = None
            if image_data is not None:
                if not isinstance(image_data, np.ndarray):
                    return FaceEnrollPredictResult(
                        message="Required numpy array in RGB/RGBA/BGR format"
                    )
                img_data = image_data
            if image_path is not None and len(image_path) > 0:
                if not os.path.exists(image_path):
                    return FaceEnrollPredictResult(
                        message=self.message.get_message(101)
                    )
                img_data = image_path_to_array(image_path, input_format=input_format)
            if img_data is None:
                return FaceEnrollPredictResult(
                    message=self.message.EXCEPTION_ERROR_ENROLL
                )

            # Check image dimensions
            if img_data.shape[0] <= 224 or img_data.shape[1] <= 224:
                return FaceEnrollPredictResult(
                    message="Image dimensions should be greater than 224x224."
                )

            return self.face_factor.enroll(image_data=img_data, config_object=config)
        except Exception as e:
            print("Oops: {}\nTrace: {}".format(e, traceback.format_exc()))
            print(
                "Issue Tracker:: \nhttps://github.com/prividentity/cryptonets-python-sdk/issues"
            )
            return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_ENROLL)

    def get_iso_face(
        self,
        image_path: str = None,
        image_data: np.array = None,
        config: ConfigObject = None,
    ) -> ISOFaceResult:
        """Takes the face image and gives back the image in ISO Spec format

        Parameters
        ----------
        image_path
            Directory path to the image file

        config (Optional)
            Additional configuration parameters for the operation

        image_data (Optional)
            Image data in numpy RGB format

        Returns
        -------
        ISOFaceResult
            status: int [0 if successful -1 if unsuccessful]

            message: str [Message from the operation]

            image: PIL.Image

            confidence: float

            iso_image_width: str

            iso_image_height: str

            iso_image_channels: str

        """
        try:
            if (
                config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in config.config_param
            ):
                input_format = config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            elif (
                self.config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in self.config.config_param
            ):
                input_format = self.config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            else:
                input_format = "rgb"
            if (image_path is not None and image_data is not None) or (
                image_path is None and image_data is None
            ):
                return ISOFaceResult(message="Specify either image_path or image_data")
            img_data = None
            if image_data is not None:
                if not isinstance(image_data, np.ndarray):
                    return ISOFaceResult(
                        message="Required numpy array in RGB/RGBA/BGR format"
                    )
                img_data = image_data
            if image_path is not None and len(image_path) > 0:
                if not os.path.exists(image_path):
                    return ISOFaceResult(message=self.message.get_message(101))
                img_data = image_path_to_array(image_path, input_format=input_format)
            if img_data is None:
                return ISOFaceResult(message=self.message.EXCEPTION_ERROR_GET_ISO_FACE)

            # Check image dimensions
            if img_data.shape[0] <= 224 or img_data.shape[1] <= 224:
                return ISOFaceResult(
                    message="Image dimensions should be greater than 224x224."
                )

            return self.face_factor.get_iso_face(
                image_data=img_data, config_object=config
            )
        except Exception as e:
            print("Oops: {}\nTrace: {}".format(e, traceback.format_exc()))
            print(
                "Issue Tracker:: \nhttps://github.com/prividentity/cryptonets-python-sdk/issues"
            )
            return ISOFaceResult(message=self.message.EXCEPTION_ERROR_GET_ISO_FACE)

    def predict(
        self,
        image_path: str = None,
        image_data: np.array = None,
        config: ConfigObject = None,
    ) -> Union[FaceEnrollPredictResult, List[FaceEnrollPredictResult]]:
        """Predicts the image in the face recognition server

        Parameters
        ----------
        image_path
            Directory path to the image file

        config (Optional)
            Additional configuration parameters for the operation

        image_data (Optional)
            Image data in numpy RGB format

        Returns
        -------
        FaceEnrollPredictResult             

        """
        try:
            if (
                config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in config.config_param
            ):
                input_format = config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            elif (
                self.config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in self.config.config_param
            ):
                input_format = self.config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            else:
                input_format = "rgb"
            if (image_path is not None and image_data is not None) or (
                image_path is None and image_data is None
            ):
                return FaceEnrollPredictResult(
                    message="Specify either image_path or image_data"
                )
            img_data = None
            if image_data is not None:
                if not isinstance(image_data, np.ndarray):
                    return FaceEnrollPredictResult(
                        message="Required numpy array in RGB/RGBA/BGR format"
                    )
                img_data = image_data
            if image_path is not None and len(image_path) > 0:
                if not os.path.exists(image_path):
                    return FaceEnrollPredictResult(
                        message=self.message.get_message(101)
                    )
                img_data = image_path_to_array(image_path, input_format=input_format)
            if img_data is None:
                return FaceEnrollPredictResult(
                    message=self.message.EXCEPTION_ERROR_PREDICT
                )

            # Check image dimensions
            if img_data.shape[0] <= 224 or img_data.shape[1] <= 224:
                return FaceEnrollPredictResult(
                    message="Image dimensions should be greater than 224x224."
                )

            return self.face_factor.predict(image_data=img_data, config_object=config)
        except Exception as e:
            print("Oops: {}\nTrace: {}".format(e, traceback.format_exc()))
            print(
                "Issue Tracker:: \nhttps://github.com/prividentity/cryptonets-python-sdk/issues"
            )
            return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_PREDICT)

    def compare_doc_with_face(
        self,
        face_path: str = None,
        doc_path: str = None,
        face_data: np.array = None,
        doc_data: np.array = None,
        config: ConfigObject = None,
    ) -> FaceCompareResult:
        """Check if the images are of same person or not

        Parameters
        ----------
        face_path
            Directory path to the face image file

        doc_path
            Directory path to the document image file

        config (Optional)
            Additional configuration parameters for the operation

        face_data (Optional)
            Face Image data in numpy RGB format

        doc_data (Optional)
            Document Image data in numpy RGB format

        Returns
        -------
        FaceCompareResult
            status: int [0 if call successful -1 if unsuccessful]

            message: str [Message from the operation]

            result: int [1 if same, -1 if different]

            distance: float [comparaison distance]

            first_validation_result: int

            second_validation_result: int

        """

        try:
            if (
                config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in config.config_param
            ):
                input_format = config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            elif (
                self.config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in self.config.config_param
            ):
                input_format = self.config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            else:
                input_format = "rgb"
            if (
                face_path is not None
                and doc_path is not None
                and face_data is not None
                and doc_data is not None
            ) or (
                face_path is None
                and doc_path is None
                and face_data is None
                and doc_data is None
            ):
                return FaceCompareResult(
                    message="Specify either image_path or image_data"
                )
            img_data_1, img_data_2 = None, None
            if doc_data is not None and face_data is not None:
                if not isinstance(face_data, np.ndarray) or not isinstance(
                    doc_data, np.ndarray
                ):
                    return FaceCompareResult(
                        message="Required numpy array in RGB/RGBA/BGR format"
                    )
                img_data_1 = face_data
                img_data_2 = doc_data
            if (face_path is not None and len(face_path) > 0) or (
                doc_path is not None and len(doc_path) > 0
            ):
                if not os.path.exists(face_path) or not os.path.exists(doc_path):
                    return FaceCompareResult(message=self.message.get_message(101))
                img_data_1 = image_path_to_array(
                    face_path, input_format=input_format
                )
                img_data_2 = image_path_to_array(
                    doc_path, input_format=input_format
                )
                if img_data_1 is None or img_data_2 is None:
                    return FaceCompareResult(
                        message=self.message.EXCEPTION_ERROR_COMPARE
                    )

            # Check image dimensions for both images
            if img_data_1.shape[0] <= 224 or img_data_1.shape[1] <= 224:
                return FaceCompareResult(
                    message="Image dimensions should be greater than 224x224."
                )
            if img_data_2.shape[0] <= 224 or img_data_2.shape[1] <= 224:
                return FaceCompareResult(
                    message="Image dimensions should be greater than 224x224."
                )

            return self.face_factor.compare_doc_with_face(
                face_data=img_data_1, doc_data=img_data_2, config_object=config
            )
        except Exception as e:
            print("Oops: {}\nTrace: {}".format(e, traceback.format_exc()))
            print(
                "Issue Tracker:: \nhttps://github.com/prividentity/cryptonets-python-sdk/issues"
            )
            return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)

    def compare(
        self,
        image_path_1: str = None,
        image_path_2: str = None,
        image_data_1: np.array = None,
        image_data_2: np.array = None,
        config: ConfigObject = None,
    ) -> FaceCompareResult:
        """Check if the images are of same person or not

        Parameters
        ----------
        image_path_1
            Directory path to the first image file

        image_path_2
            Directory path to the second image file

        config (Optional)
            Additional configuration parameters for the operation

        image_data_1 (Optional)
            First Image data in numpy RGB format

        image_data_2 (Optional)
            Second Image data in numpy RGB format

        Returns
        -------
        FaceCompareResult
            status: int [0 if call successful -1 if unsuccessful]

            message: str [Message from the operation]

            result: int [1 if same, -1 if different]

            distance: float [comparaison distance]

            first_validation_result: int

            second_validation_result: int

        """

        try:
            if (
                config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in config.config_param
            ):
                input_format = config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            elif (
                self.config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in self.config.config_param
            ):
                input_format = self.config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            else:
                input_format = "rgb"
            if (
                image_path_1 is not None
                and image_path_2 is not None
                and image_data_1 is not None
                and image_data_2 is not None
            ) or (
                image_path_1 is None
                and image_path_2 is None
                and image_data_1 is None
                and image_data_2 is None
            ):
                return FaceCompareResult(
                    message="Specify either image_path or image_data"
                )
            img_data_1, img_data_2 = None, None
            if image_data_1 is not None and image_data_2 is not None:
                if not isinstance(image_data_1, np.ndarray) or not isinstance(
                    image_data_2, np.ndarray
                ):
                    return FaceCompareResult(
                        message="Required numpy array in RGB/RGBA/BGR format"
                    )
                img_data_1 = image_data_1
                img_data_2 = image_data_2
            if (image_path_1 is not None and len(image_path_1) > 0) or (
                image_path_2 is not None and len(image_path_2) > 0
            ):
                if not os.path.exists(image_path_1) or not os.path.exists(image_path_2):
                    return FaceCompareResult(message=self.message.get_message(101))
                img_data_1 = image_path_to_array(
                    image_path_1, input_format=input_format
                )
                img_data_2 = image_path_to_array(
                    image_path_2, input_format=input_format
                )
                if img_data_1 is None or img_data_2 is None:
                    return FaceCompareResult(
                        message=self.message.EXCEPTION_ERROR_COMPARE
                    )

            # Check image dimensions for both images
            if img_data_1.shape[0] <= 224 or img_data_1.shape[1] <= 224:
                return FaceCompareResult(
                    message="Image dimensions should be greater than 224x224."
                )
            if img_data_2.shape[0] <= 224 or img_data_2.shape[1] <= 224:
                return FaceCompareResult(
                    message="Image dimensions should be greater than 224x224."
                )

            return self.face_factor.compare(
                image_data_1=img_data_1, image_data_2=img_data_2, config_object=config
            )
        except Exception as e:
            print("Oops: {}\nTrace: {}".format(e, traceback.format_exc()))
            print(
                "Issue Tracker:: \nhttps://github.com/prividentity/cryptonets-python-sdk/issues"
            )
            return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)
    def antispoof_check(
        self,
        image_path: str = None,
        image_data: np.array = None,
        config: ConfigObject = None,
    ) -> AntispoofCheckResult:
        """Check if the image is spoofed or not

        Parameters
        ----------
        image_path
            Directory path to the image file

        config (Optional)
            Additional configuration parameters for the operation

        image_data (Optional)
            Image data in numpy RGB format

        Returns
        -------
        AntispoofCheckResult

            status: int [0 if successful -1 if unsuccessful]
            
            message: str [Message from the operation]

            is_antispoof: bool [True if spoofed, False if not spoofed]
        
        """
        try:
            if (
                config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in config.config_param
            ):
                input_format = config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            elif (
                self.config is not None
                and PARAMETERS.INPUT_IMAGE_FORMAT in self.config.config_param
            ):
                input_format = self.config.config_param[PARAMETERS.INPUT_IMAGE_FORMAT]
            else:
                input_format = "rgb"
            if (image_path is not None and image_data is not None) or (
                image_path is None and image_data is None
            ):
                return AntispoofCheckResult(
                    message="Specify either image_path or image_data"
                )
            img_data = None
            if image_data is not None:
                if not isinstance(image_data, np.ndarray):
                    return AntispoofCheckResult(
                        message="Required numpy array in RGB/RGBA/BGR format"
                    )
                img_data = image_data
            if image_path is not None and len(image_path) > 0:
                if not os.path.exists(image_path):
                    return AntispoofCheckResult(message=self.message.get_message(101))
                img_data = image_path_to_array(image_path, input_format=input_format)
            if img_data is None:
                return AntispoofCheckResult(message=self.message.ANTISPOOF_CHECK_ERROR)

            # Check image dimensions
            if img_data.shape[0] <= 224 or img_data.shape[1] <= 224:
                return AntispoofCheckResult(
                    message="Image dimensions should be greater than 224x224."
                )

            return self.face_factor.antispoof_check(
                image_data=img_data, config_object=config
            )
        except Exception as e:
            print("Oops: {}\nTrace: {}".format(e, traceback.format_exc()))
            print(
                "Issue Tracker:: \nhttps://github.com/prividentity/cryptonets-python-sdk/issues"
            )
            return AntispoofCheckResult(message=self.message.ANTISPOOF_CHECK_ERROR)

    def delete(self, puid: str ,config_object: ConfigObject = None ) -> FaceDeleteResult:
        """Deletes a user by their PUID from the system

        Parameters
        ----------
        puid : str
            The PUID (Private User ID) of the user to delete
        
        config_object : ConfigObject (Optional)
            Additional configuration parameters for the operation

        Returns
        -------
        FaceDeleteResult
            Result of the delete operation
        """
        if puid is None:
            return FaceDeleteResult(message=self.message.MISSING_ARGUMENT.format("puid"))   
        elif puid == '':
            return FaceDeleteResult(message=self.message.INVALID_ARGUMENT.format("puid"))
        
        try:
            return self.face_factor.delete(puid,config_object=config_object)
        except Exception as e:
            import traceback
            print(f"Delete operation failed: {e}\nTrace: {traceback.format_exc()}")
            print(
                "Issue Tracker:: \nhttps://github.com/prividentity/cryptonets-python-sdk/issues"
            )
            return FaceDeleteResult(status=-1, message=self.message.EXCEPTION_ERROR_DELETE)


    @property
    def api_key(self) -> str:
        return self._api_key

    @property
    def server_url(self) -> str:
        return self._server_url
    
    @property
    def logging_level(self) -> LoggingLevel:
        return self._logging_level

    @property
    def config(self) -> ConfigObject:
        return self._config_object

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    @server_url.setter
    def server_url(self, value):
        self._server_url = value
    
    @logging_level.setter
    def logging_level(self, value):
        self._logging_level = value

    @config.setter
    def config(self, value):
        self._config_object = value    


if __name__ == "__main__":
    pass

"""Factor implements the functionalities of each factors to generate and verify Private IDs .
"""
import os
import pathlib
import traceback
from typing import Any

import numpy as np

from .helper.decorators import Singleton, deprecated
from .factor_modules.FaceModule import Face
from .helper.result_objects.compareResult import FaceCompareResult
from .helper.result_objects.deleteResult import FaceDeleteResult
from .helper.result_objects.enrollPredictResult import FaceEnrollPredictResult
from .helper.result_objects.isValidDeprecatedResult import FaceIsValidDeprecatedResult
from .helper.result_objects.isValidResult import FaceIsValidResult
from .helper.result_objects.ageEstimateResult import FaceAgeResult
from .helper.messages import Message
from .helper.utils import image_path_to_array
from .settings.loggingLevel import LoggingLevel


class FaceFactor(metaclass=Singleton):
    """The FaceFactor class implements the methods for enrolling and predicting the Face module as part of the
        Biometric Authentication.

        It exposes five methods as part of the interface:

        1. is_valid: Verifies the face of the user.
        2. estimate_age: Predicts the age of the face.
        3. compare: Compare two faces for verification.
        4. enroll: Enrolls the face of the user.
        5. predict: Predicts the face of the user.
        6. delete: Deletes the user from the system

        Check out the :ref:`return codes <return_codes>` section for complete list of return codes.

        Parameters
        ----------
        server_url : str
            The URL of the FaceFactor server.

        local_storage_path : str (optional)
            Absolute path to the local storage.

        api_key : str
            The API key for using the FaceFactor server.

        logging_level : Object (Optional)
            LoggingLevel needed while performing operation

        Returns
        -------
        object
            Instance of the FaceFactor class.

        Methods
        -------
        is_valid
        estimate_age
        compare
        enroll
        predict
        delete
    """

    def __init__(self, server_url, local_storage_path=None, api_key=None, logging_level: Any = LoggingLevel.off.value):
        if server_url is None:
            raise Exception("Server URL has to be configured")
        if api_key is None:
            raise Exception("API Key is required.")
        self.server_url = server_url
        self.api_key = api_key
        if local_storage_path is None:
            self.local_storage_path = str(pathlib.Path(__file__).joinpath("privateid_local_storage").resolve())
        else:
            self.local_storage_path = local_storage_path
        self.face_factor = Face(
            url=self.server_url, local_storage_path=self.local_storage_path, api_key=self.api_key,
            logging_level=logging_level)
        self.message = Message()

    @deprecated
    def is_valid_deprecated(self, image_path: str = None, image_data: np.array = None) -> FaceIsValidDeprecatedResult:
        """Check if the image is valid for using in the face recognition
        Deprecated: Use the is_valid instead as it improves the processing speed of is valid.

        Parameters
        ----------
        image_path
            Directory path to the image file

        image_data(optional)
            Image data in numpy RGB format

        Returns
        -------
        FaceIsValidResult
            status: int [0 if successful -1 if unsuccessful]

            message: str [Message from the operation]

            result: str [Result of the operation]

            age_factor: str [Predicted age of the image]

            output_image_data: any [Numpy RGB image data of cropped face]

        """
        try:
            if (image_path is not None and image_data is not None) or (image_path is None and image_data is None):
                return FaceIsValidDeprecatedResult(message="Specify either image_path or image_data")
            img_data = None
            if image_data is not None:
                if not isinstance(image_data, np.ndarray):
                    return FaceIsValidDeprecatedResult(message="Required numpy array in RGB format")
                img_data = image_data
            if image_path is not None and len(image_path) > 0:
                if not os.path.exists(image_path):
                    return FaceIsValidDeprecatedResult(message=self.message.get_message(101))
                img_data = image_path_to_array(image_path)
            if img_data is None:
                return FaceIsValidDeprecatedResult(message=self.message.IS_VALID_ERROR)
            return self.face_factor.is_valid_deprecated(image_data=img_data)
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceIsValidDeprecatedResult(message=self.message.IS_VALID_ERROR)

    def is_valid(self, image_path: str = None, image_data: np.array = None) -> FaceIsValidResult:
        """Check if the image is valid for using in the face recognition

        Parameters
        ----------
        image_path
            Directory path to the image file

        image_data(optional)
            Image data in numpy RGB format

        Returns
        -------
        FaceIsValidResult
            status: int

            message: str [Message from the operation]


        """
        try:
            if (image_path is not None and image_data is not None) or (image_path is None and image_data is None):
                return FaceIsValidResult(message="Specify either image_path or image_data")
            img_data = None
            if image_data is not None:
                if not isinstance(image_data, np.ndarray):
                    return FaceIsValidResult(message="Required numpy array in RGB format")
                img_data = image_data
            if image_path is not None and len(image_path) > 0:
                if not os.path.exists(image_path):
                    return FaceIsValidResult(message=self.message.get_message(101))
                img_data = image_path_to_array(image_path)
            if img_data is None:
                return FaceIsValidResult(message=self.message.IS_VALID_ERROR)
            return self.face_factor.is_valid(image_data=img_data)
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceIsValidResult(message=self.message.IS_VALID_ERROR)

    def estimate_age(self, image_path: str, image_data: np.array = None) -> FaceAgeResult:
        """Check if the image is valid and returns the age of the image

        Parameters
        ----------
        image_path
            Directory path to the image file

        image_data(optional)
            Image data in numpy RGB format

        Returns
        -------
        FaceAgeResult
            status: int

            message: str [Message from the operation]

            age: float [As returned from the model directly]
        """
        try:
            if (image_path is not None and image_data is not None) or (image_path is None and image_data is None):
                return FaceAgeResult(message="Specify either image_path or image_data")
            img_data = None
            if image_data is not None:
                if not isinstance(image_data, np.ndarray):
                    return FaceAgeResult(message="Required numpy array in RGB format")
                img_data = image_data
            if image_path is not None and len(image_path) > 0:
                if not os.path.exists(image_path):
                    return FaceAgeResult(message=self.message.get_message(101))
                img_data = image_path_to_array(image_path)
            if img_data is None:
                return FaceAgeResult(message=self.message.AGE_ESTIMATE_ERROR)
            return self.face_factor.estimate_age(image_data=img_data)
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceAgeResult(message=self.message.AGE_ESTIMATE_ERROR)

    def enroll(self, image_path: str = None, image_data: np.array = None) -> FaceEnrollPredictResult:
        """Enrolls the image in the face recognition server

        Parameters
        ----------
        image_path
            Directory path to the image file

        image_data (optional)
            Image data in numpy RGB format

        Returns
        -------
        FaceEnrollPredictResult
            status: int [0 if successful -1 if unsuccessful]

            message: str [Message from the operation]

            enroll_level: str

            guid: str

            uuid: str

            token: str
        """

        try:
            if (image_path is not None and image_data is not None) or (image_path is None and image_data is None):
                return FaceEnrollPredictResult(message="Specify either image_path or image_data")
            img_data = None
            if image_data is not None:
                if not isinstance(image_data, np.ndarray):
                    return FaceEnrollPredictResult(message="Required numpy array in RGB format")
                img_data = image_data
            if image_path is not None and len(image_path) > 0:
                if not os.path.exists(image_path):
                    return FaceEnrollPredictResult(message=self.message.get_message(101))
                img_data = image_path_to_array(image_path)
            if img_data is None:
                return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_ENROLL)
            return self.face_factor.enroll(image_data=img_data)
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_ENROLL)

    def predict(self, image_path: str = None, image_data: np.array = None) -> FaceEnrollPredictResult:
        """Predicts the image in the face recognition server

        Parameters
        ----------
        image_path
            Directory path to the image file

        image_data (optional)
            Image data in numpy RGB format

        Returns
        -------
        FaceEnrollPredictResult
            status: int [0 if successful -1 if unsuccessful]

            message: str [Message from the operation]

            enroll_level: str

            guid: str

            uuid: str

            token: str

        """
        try:
            if (image_path is not None and image_data is not None) or (image_path is None and image_data is None):
                return FaceEnrollPredictResult(message="Specify either image_path or image_data")
            img_data = None
            if image_data is not None:
                if not isinstance(image_data, np.ndarray):
                    return FaceEnrollPredictResult(message="Required numpy array in RGB format")
                img_data = image_data
            if image_path is not None and len(image_path) > 0:
                if not os.path.exists(image_path):
                    return FaceEnrollPredictResult(message=self.message.get_message(101))
                img_data = image_path_to_array(image_path)
            if img_data is None:
                return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_PREDICT)
            return self.face_factor.predict(image_data=img_data)
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_PREDICT)

    def delete(self, uuid: str) -> FaceDeleteResult:
        """Deletes the enrollment from the face recognition server

        Parameters
        ----------
        uuid
            UUID of the enrolled image

        Returns
        -------
        FaceDeleteResult
            status: int [0 if successful -1 if unsuccessful]

            message: str [Message from the operation]
        """
        try:
            if uuid is None:
                return FaceDeleteResult(message="Missing UUID")
            return self.face_factor.delete(uuid)
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceDeleteResult(message=self.message.EXCEPTION_ERROR_DELETE)

    def compare(self, image_path_1: str = None, image_path_2: str = None, image_data_1: np.array = None,
                image_data_2: np.array = None) -> FaceCompareResult:
        """Check if the images are of same person or not

        Parameters
        ----------
        image_path_1
            Directory path to the first image file

        image_path_2
            Directory path to the second image file

        image_data_1 (Optional)
            First Image data in numpy RGB format

        image_data_2 (Optional)
            Second Image data in numpy RGB format

        Returns
        -------
        FaceCompareResult
            status: int [0 if same, 1 if different, -1 if unsuccessful]

            message: str [Message from the operation]

            result: str

            distance_min: str

            distance_mean: str

            distance_max: str

            first_validation_result: str

            second_validation_result: str

        """

        try:

            if (image_path_1 is not None and image_path_2 is not None and
                image_data_1 is not None and image_data_2 is not None) or (
                    image_path_1 is None and image_path_2 is None and image_data_1 is None and image_data_2 is None):
                return FaceCompareResult(message="Specify either image_path or image_data")
            img_data_1, img_data_2 = None, None
            if image_data_1 is not None and image_data_2 is not None:
                if not isinstance(image_data_1, np.ndarray) or not isinstance(image_data_2, np.ndarray):
                    return FaceCompareResult(message="Required numpy array in RGB format")
                img_data_1 = image_data_1
                img_data_2 = image_data_2
            if (image_path_1 is not None and len(image_path_1) > 0) \
                    or (image_path_2 is not None and len(image_path_2) > 0):
                if not os.path.exists(image_path_1) or not os.path.exists(image_path_2):
                    return FaceCompareResult(message=self.message.get_message(101))
                img_data_1 = image_path_to_array(image_path_1)
                img_data_2 = image_path_to_array(image_path_2)
            if img_data_1 is None or img_data_2 is None:
                return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)
            return self.face_factor.compare(image_data_1=img_data_1, image_data_2=img_data_2)
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)


if __name__ == "__main__":
    pass

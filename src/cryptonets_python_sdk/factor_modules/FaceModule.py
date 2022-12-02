import traceback

from typing import List
from typing import Any

import numpy as np

from ..handler.nativeMethods import NativeMethods
from ..helper.decorators import Singleton, deprecated
from ..helper.messages import Message
from ..helper.result_objects.compareResult import FaceCompareResult
from ..helper.result_objects.deleteResult import FaceDeleteResult
from ..helper.result_objects.enrollPredictResult import FaceEnrollPredictResult
from ..helper.result_objects.isValidDeprecatedResult import FaceIsValidDeprecatedResult
from ..helper.result_objects.faceValidationResult import FaceValidationResult

from ..helper.utils import FaceValidationCode


class Face(metaclass=Singleton):

    def __init__(self, url: str, local_storage_path: str, api_key: str, logging_level: Any):
        self.message = Message()
        self.face_factor_processor = NativeMethods(api_key=api_key, url=url, local_storage_path=local_storage_path,
                                                   logging_level=logging_level)

    def enroll(self, image_data: np.array) -> FaceEnrollPredictResult:
        try:
            json_data = self.face_factor_processor.enroll(image_data)
            if not json_data:
                return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_ENROLL)
            if "PI" not in json_data:
                return FaceEnrollPredictResult(status=json_data.get("status", -1),
                                               message=json_data.get("message", self.message.EXCEPTION_ERROR_ENROLL))
            return FaceEnrollPredictResult(enroll_level=json_data["PI"].get("enroll_level", None),
                                           uuid=json_data["PI"].get("uuid", None),
                                           guid=json_data["PI"].get("guid", None),
                                           token=json_data["PI"].get("token", None), status=json_data.get("status", -1),
                                           message=json_data.get("message", ""))
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_ENROLL)

    def predict(self, image_data: np.array) -> FaceEnrollPredictResult:
        try:
            json_data = self.face_factor_processor.predict(image_data)
            if not json_data:
                return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_PREDICT)
            if "PI" not in json_data:
                return FaceEnrollPredictResult(status=json_data.get("status", -1),
                                               message=json_data.get("message", self.message.EXCEPTION_ERROR_PREDICT))
            return FaceEnrollPredictResult(enroll_level=json_data["PI"].get("enroll_level", None),
                                           uuid=json_data["PI"].get("uuid", None),
                                           guid=json_data["PI"].get("guid", None),
                                           token=json_data["PI"].get("token", None), status=json_data.get("status", -1),
                                           message=json_data.get("message", ""))
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_PREDICT)

    def delete(self, uuid: str) -> FaceDeleteResult:
        try:
            json_response = self.face_factor_processor.delete(uuid)
            if not json_response:
                return FaceDeleteResult(message=self.message.EXCEPTION_ERROR_DELETE)
            return FaceDeleteResult(status=json_response.get("status", -1), message=json_response.get("message", ""))
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceDeleteResult(message=self.message.EXCEPTION_ERROR_DELETE)

    def compare(self, image_data_1: np.array, image_data_2: np.array) -> FaceCompareResult:
        try:
            json_data = self.face_factor_processor.compare_files(image_data_1, image_data_2)
            if not json_data:
                return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)

            return FaceCompareResult(result=json_data.get("result", None),
                                     distance_min=json_data.get("distance_min", None),
                                     first_validation_result=json_data.get("valid_flag_a", None),
                                     second_validation_result=json_data.get("valid_flag_b", None),
                                     distance_max=json_data.get("distance_max", None),
                                     distance_mean=json_data.get("distance_mean", None),
                                     status=json_data.get("status", 1), message=json_data.get("message", ""))
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)

    @deprecated
    def is_valid_deprecated(self, image_data: np.array) -> FaceIsValidDeprecatedResult:
        try:
            json_data = self.face_factor_processor.is_valid(image_data)
            if not json_data:
                return FaceIsValidDeprecatedResult(message=self.message.IS_VALID_ERROR)

            result_ = None
            if json_data.get("result", None) in FaceValidationCode:
                result_ = FaceValidationCode(json_data.get("result", None)).name

            return FaceIsValidDeprecatedResult(result=result_, age_factor=json_data.get("ageFactor", None), status=0)

        except Exception as e:
            print(e, traceback.format_exc())
            return FaceIsValidDeprecatedResult(message=self.message.IS_VALID_ERROR)

    def is_valid(self, image_data: np.array) -> FaceValidationResult:
        try:
            json_data = self.face_factor_processor.is_valid_without_age(image_data)
            if not json_data:
                return FaceValidationResult(message=self.message.IS_VALID_ERROR)

            if json_data.get("error", -100) != 0:
                return FaceValidationResult(error=json_data.get("error", -100), message=self.message.IS_VALID_ERROR)

            face_validate_result_object = FaceValidationResult(error=json_data.get("error", -1), message="OK")
            for face in json_data.get("faces", []):
                _return_code = face.get("status", -100)
                if _return_code in FaceValidationCode:
                    _message = FaceValidationCode(_return_code).name
                else:
                    raise Exception("Status code out of bounds.")
                face_validate_result_object.append_face_objects(return_code=_return_code, message=_message,
                                                                top_left_coordinate=face["box"].get("top_left", None),
                                                                bottom_right_coordinate=face["box"].get("bottom_right",
                                                                                                        None))

            return face_validate_result_object
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceValidationResult(message=self.message.IS_VALID_ERROR)

    def estimate_age(self, image_data: np.array) -> FaceValidationResult:
        try:
            json_data = self.face_factor_processor.estimate_age(image_data)
            if not json_data:
                return FaceValidationResult(message=self.message.AGE_ESTIMATE_ERROR)

            if json_data.get("error", -1) != 0:
                return FaceValidationResult(error=json_data.get("error", -1), message=self.message.AGE_ESTIMATE_ERROR)

            face_age_result_object = FaceValidationResult(error=json_data.get("error", -1), message="OK")
            for face in json_data.get("faces"):

                _return_code = face.get("status", -1)
                _age = face.get("age", -1.0)
                if _return_code in FaceValidationCode:
                    _message = FaceValidationCode(_return_code).name
                else:
                    raise Exception("Status code out of bounds.")
                if _return_code == -1:
                    _age = -1
                    _message = "Please validate the images using isvalid function"
                face_age_result_object.append_face_objects(return_code=_return_code, age=_age, message=_message,
                                                           top_left_coordinate=face["box"].get("top_left", None),
                                                           bottom_right_coordinate=face["box"].get("bottom_right",
                                                                                                   None))

            return face_age_result_object
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceValidationResult(message=self.message.AGE_ESTIMATE_ERROR)

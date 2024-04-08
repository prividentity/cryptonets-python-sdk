import string
import traceback
from typing import Union, List
import numpy as np

from ..handler.nativeMethods import NativeMethods
from ..helper.decorators import Singleton
from ..helper.messages import Message
from ..helper.result_objects.compareResult import FaceCompareResult
from ..helper.result_objects.deleteResult import FaceDeleteResult
from ..helper.result_objects.enrollPredictResult import FaceEnrollPredictResult
from ..helper.result_objects.faceValidationResult import FaceValidationResult
from ..helper.result_objects.isoFaceResult import ISOFaceResult
from ..helper.utils import FaceValidationCode
from ..settings.cacheType import CacheType
from ..settings.configuration import ConfigObject
from ..settings.loggingLevel import LoggingLevel


class Face(metaclass=Singleton):
    def __init__(
        self,
        api_key: str,
        server_url: str,
        local_storage_path: str,
        logging_level: LoggingLevel,
        tf_num_thread: int,
        cache_type: CacheType,
        config_object: ConfigObject = None,
    ):
        self.message = Message()
        self.face_factor_processor = NativeMethods(
            api_key=api_key,
            server_url=server_url,
            local_storage_path=local_storage_path,
            logging_level=logging_level,
            tf_num_thread=tf_num_thread,
            cache_type=cache_type,
            config_object=config_object,
        )

    def update_config(self, config_object):
        self.face_factor_processor.update_config(config_object=config_object)

    def enroll(
        self, image_data: np.array, config_object: ConfigObject = None
    ) -> FaceEnrollPredictResult:
        try:
            json_data = self.face_factor_processor.enroll(
                image_data, config_object=config_object
            )
            call_status = FaceEnrollPredictResult.CALL_STATUS_ERROR
            if not json_data:
                return FaceEnrollPredictResult(
                    message=self.message.EXCEPTION_ERROR_ENROLL
                )
            else:
                # we received a json response and thus call is successful
                call_status = FaceEnrollPredictResult.CALL_STATUS_SUCCESS

            api_response=json_data.get("enroll_onefa", {}).get("api_response", {});
            return FaceEnrollPredictResult(
                status=call_status,
                enroll_level=json_data.get("enroll_level", None),
                puid=api_response.get("puid", None),
                guid=api_response.get("guid", None),
                token=api_response.get("token", None),
                score=api_response.get("score", None),
                message=api_response.get("message", ""),
            )
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_ENROLL)

    def predict(
        self, image_data: np.array, config_object: ConfigObject = None
    ) -> Union[FaceEnrollPredictResult, List[FaceEnrollPredictResult]]:
        try:
            json_data = self.face_factor_processor.predict(
                image_data, config_object=config_object
            )
            call_status = FaceEnrollPredictResult.CALL_STATUS_ERROR
            if not json_data:
                return FaceEnrollPredictResult(
                    message=self.message.EXCEPTION_ERROR_PREDICT
                )
            else:
                # we received a json response and thus call is successful
                call_status = FaceEnrollPredictResult.CALL_STATUS_SUCCESS

            api_response=json_data.get("predict_onefa", {}).get("api_response", {});
            if not api_response.get("PI_list", []):
                return FaceEnrollPredictResult(
                    status=call_status,
                    enroll_level=json_data.get("enroll_level", None),
                    puid=api_response.get("puid", None),
                    guid=api_response.get("guid", None),
                    token=api_response.get("token", None),
                    score=api_response.get("score", None),
                    message=api_response.get("message", ""),
                )
            else:
                return [FaceEnrollPredictResult(
                    status=call_status,
                    enroll_level=json_data.get("enroll_level", None),
                    puid=person.get("puid", None),
                    guid=person.get("guid", None),
                    score=person.get("score", None),
                    message=api_response.get("message", "Something went wrong"),
                ) for person in api_response.get("PI_list", [])]
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_PREDICT)

    def delete(self, puid: str, config_object: ConfigObject = None,) -> FaceDeleteResult:
        try:
            json_response = self.face_factor_processor.delete(puid,config_object)
            if not json_response:
                return FaceDeleteResult(message=self.message.EXCEPTION_ERROR_DELETE)
            return FaceDeleteResult(
                status=json_response.get("status", -1),
                message=json_response.get("message", ""),
            )
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceDeleteResult(message=self.message.EXCEPTION_ERROR_DELETE)
     
    def _doc_scan_face(self, image_data: np.array, config_object: ConfigObject = None):
        try:
            json_data = self.face_factor_processor.doc_scan_face(
                image_data, config_object=config_object
            )
            return json_data
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_PREDICT)



    def compare_doc_with_face(
        self,
        face_data: np.array,
        doc_data: np.array,
        config_object: ConfigObject = None,
    ) -> FaceCompareResult:
        try:
            processed_document=self._doc_scan_face(image_data=doc_data)
            if processed_document.get("doc_face",{}).get("document_data",{}).get("document_validation_status",-1)!=0:
                 return FaceCompareResult(message= processed_document.get("doc_face",{}).get("document_data",{}).get("status_message","Something went wrong"))
            from PIL import Image

            cropped_face_array = processed_document.get("doc_face",{}).get("cropped_face")
            print(processed_document.get("doc_face",{}))
            if cropped_face_array is not None:
                print(cropped_face_array)
                cropped_face_image = Image.fromarray(cropped_face_array)
                cropped_face_image.save("cropped_face_debug_2.png")  
            
            json_data_all = self.face_factor_processor.compare_files(
                face_data, processed_document.get("doc_face",{}).get("cropped_face"), config_object=config_object
            )

            call_status = FaceCompareResult.CALL_STATUS_ERROR
            if not json_data_all:
                return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)
            else:
                # we received a json response and thus call is successful
                call_status = FaceCompareResult.CALL_STATUS_SUCCESS
            json_data=json_data_all.get("face_compare",{})
            return FaceCompareResult(
                result=json_data.get("result", None),
                distance_min=json_data.get("distance_min", None),
                first_validation_result=json_data.get("valid_flag_a", None),
                second_validation_result=json_data.get("valid_flag_b", None),
                distance_max=json_data.get("distance_max", None),
                distance_mean=json_data.get("distance_mean", None),
                status=call_status,
                message=json_data.get("message", ""),
            )
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)

    def compare(
        self,
        image_data_1: np.array,
        image_data_2: np.array,
        config_object: ConfigObject = None,
    ) -> FaceCompareResult:
        try:
            json_data = self.face_factor_processor.compare_files(
                image_data_1, image_data_2, config_object=config_object
            )
            call_status = FaceCompareResult.CALL_STATUS_ERROR
            if not json_data:
                return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)
            else:
                # we received a json response and thus call is successful
                call_status = FaceCompareResult.CALL_STATUS_SUCCESS

            return FaceCompareResult(
                result=json_data.get("result", None),
                distance_min=json_data.get("distance_min", None),
                first_validation_result=json_data.get("valid_flag_a", None),
                second_validation_result=json_data.get("valid_flag_b", None),
                distance_max=json_data.get("distance_max", None),
                distance_mean=json_data.get("distance_mean", None),
                status=call_status,
                message=json_data.get("message", ""),
            )
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)

    def is_valid(
        self, image_data: np.array, config_object: ConfigObject = None
    ) -> FaceValidationResult:
        try:
            json_data = self.face_factor_processor.is_valid_without_age(
                image_data, config_object=config_object
            )
            if not json_data:
                return FaceValidationResult(message=self.message.IS_VALID_ERROR)

            if json_data.get("error", -100) != 0:
                return FaceValidationResult(
                    error=json_data.get("error", -100),
                    message=self.message.IS_VALID_ERROR,
                )

            face_validate_result_object = FaceValidationResult(
                error=json_data.get("error", -1), message="OK"
            )
            for face in json_data.get("faces", []):
                _return_code = face.get("status", -100)
                if _return_code in FaceValidationCode:
                    _message = FaceValidationCode(_return_code).name
                else:
                    raise Exception("Status code out of bounds.")
                face_validate_result_object.append_face_objects(
                    return_code=_return_code,
                    message=_message,
                    top_left_coordinate=face["box"].get("top_left", None),
                    bottom_right_coordinate=face["box"].get("bottom_right", None),
                )

            return face_validate_result_object
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceValidationResult(message=self.message.IS_VALID_ERROR)

    def estimate_age(
        self, image_data: np.array, config_object: ConfigObject = None
    ) -> FaceValidationResult:
        try:
            json_data = self.face_factor_processor.estimate_age(
                image_data, config_object=config_object
            )
            if not json_data:
                return FaceValidationResult(message=self.message.AGE_ESTIMATE_ERROR)

            if json_data.get("error", -1) != 0:
                return FaceValidationResult(
                    error=json_data.get("error", -1),
                    message=self.message.AGE_ESTIMATE_ERROR,
                )

            face_age_result_object = FaceValidationResult(
                error=json_data.get("error", -1), message="OK"
            )
            for face in json_data.get("faces"):

                _return_code = face.get("status", -1)
                _age = face.get("age", -1.0)
                if _return_code in FaceValidationCode:
                    _message = FaceValidationCode(_return_code).name
                else:
                    raise Exception("Status code out of bounds.")
                if _return_code == -1:
                    _age = -1
                face_age_result_object.append_face_objects(
                    return_code=_return_code,
                    age=_age,
                    message=_message,
                    top_left_coordinate=face["box"].get("top_left", None),
                    bottom_right_coordinate=face["box"].get("bottom_right", None),
                )

            return face_age_result_object
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceValidationResult(message=self.message.AGE_ESTIMATE_ERROR)

    def get_iso_face(
        self, image_data: np.array, config_object: ConfigObject = None
    ) -> ISOFaceResult:
        try:
            json_data = self.face_factor_processor.get_iso_face(
                image_data, config_object=config_object
            )
            if not json_data:
                return ISOFaceResult(message=self.message.EXCEPTION_ERROR_GET_ISO_FACE)

            if json_data.get("status", -1) != 0:
                return ISOFaceResult(
                    status=json_data.get("status", -1),
                    message=self.message.EXCEPTION_ERROR_GET_ISO_FACE,
                )

            return ISOFaceResult(
                iso_image_width=json_data.get("iso_image_width", None),
                iso_image_height=json_data.get("iso_image_height", None),
                iso_image_channels=json_data.get("iso_image_channels", None),
                confidence=json_data.get("confidence", None),
                image=json_data.get("image", None),
                status=json_data.get("status", -1),
                message=json_data.get("message", "OK"),
            )

        except Exception as e:
            print(e, traceback.format_exc())
            return ISOFaceResult(message=self.message.EXCEPTION_ERROR_GET_ISO_FACE)

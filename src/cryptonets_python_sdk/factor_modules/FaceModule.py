import string
import traceback

from typing import Union, List, Optional
import numpy as np
import json
from ..handler.nativeMethods import NativeMethods
from ..helper.decorators import Singleton
from ..helper.messages import Message
from ..helper.result_objects.compareResult import FaceCompareResult
from ..helper.result_objects.deleteResult import FaceDeleteResult
from ..helper.result_objects.enrollPredictResult import FaceEnrollPredictResult
from ..helper.result_objects.faceValidationResult import FaceValidationResult
from ..helper.result_objects.isoFaceResult import ISOFaceResult
from ..helper.result_objects.antispoofCheckResult import AntispoofCheckResult
from ..helper.utils import FaceValidationCode
from ..settings.cacheType import CacheType
from ..settings.configuration import ConfigObject, PARAMETERS
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
            relax_face_validation = False
            if (PARAMETERS.RELAX_FACE_VALIDATION in config_object.config_param):
                relax_face_validation = config_object.config_param[PARAMETERS.RELAX_FACE_VALIDATION]
                if relax_face_validation not in [True, False]:# this will aise exception
                    raise ValueError(
                        "Invalid key value pair\n'{}' : '{}'".format(
                            PARAMETERS.RELAX_FACE_VALIDATION, relax_face_validation
                        )
                    )
            
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

            c_response=json_data.get("enroll_onefa", {})
            api_response=c_response.get("api_response", {})
            face_validation_data=c_response.get("face_validation_data", {})
            api_response=c_response.get("api_response", {})
            result =  FaceEnrollPredictResult(
                status=call_status,
                enroll_level=json_data.get("enroll_level", None),
                puid=api_response.get("puid", None),
                guid=api_response.get("guid", None),
                token=api_response.get("token", None),
                score=api_response.get("score", None),
                message=self.message.get_message(int(face_validation_data.get("face_validation_status",0)))
            )
            result.api_message=api_response.get("message", "")
            result.api_status=api_response.get("status",-1)
            result.enroll_performed=c_response.get("enroll_performed", False)
            # If the face was successfully enrolled no need to show any message about face validation 
            # status unlike the native SDK and return a success status
            if result.enroll_performed: 
                result.status = FaceEnrollPredictResult.CALL_STATUS_SUCCESS
            
            if not result.enroll_performed and not relax_face_validation:
                result.status = face_validation_data.get("face_validation_status",0)

            if result.enroll_performed or relax_face_validation:
                result.message = ""            
            
            return result
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_ENROLL)
        

    def _valid_uuid(self,uuid):        
        try :
            if uuid is None: return False
            str_uuid = uuid[0] if isinstance(uuid, tuple) else uuid
            if not isinstance(str_uuid, str): return False
            if len(str_uuid) == 0 : return False            
            if str_uuid == "null" or str_uuid == "None"  or str_uuid == "NULL"  or str_uuid == "none" or str_uuid == "Null": return False            
            return True
        except:
            return False

    def predict(
        self, image_data: np.array, config_object: ConfigObject = None
    ) -> Union[FaceEnrollPredictResult, List[FaceEnrollPredictResult]]:
        try:
            relax_face_validation = False
            if (PARAMETERS.RELAX_FACE_VALIDATION in config_object.config_param):
                relax_face_validation = config_object.config_param[PARAMETERS.RELAX_FACE_VALIDATION]
                if relax_face_validation not in [True, False]:# this will aise exception
                    raise ValueError(
                        "Invalid key value pair\n'{}' : '{}'".format(
                            PARAMETERS.RELAX_FACE_VALIDATION, relax_face_validation
                        )
                    )
                                
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

            c_response=json_data.get("predict_onefa", {})
            api_response=c_response.get("api_response", {})
            face_validation_data=c_response.get("face_validation_data", {})            
            message = self.message.get_message(face_validation_data.get("face_validation_status", 0))
            # Did we have a successful predict
            predicted = False
            api_status = api_response.get("status",-1)
            puid=api_response.get("puid", None),
            guid=api_response.get("guid", None),
            predicted = api_status == 0 and self._valid_uuid(puid) and self._valid_uuid(guid)           
            result_status =  0 if relax_face_validation or predicted else face_validation_data.get("face_validation_status",0)
            if face_validation_data.get("face_validation_status",0)!=0:
                if config_object and json.loads(config_object.get_config_param()).get("neighbors",0)>0:
                        if api_response.get("PI_list", []):
                            return [FaceEnrollPredictResult(
                            status=face_validation_data.get("face_validation_status",0),
                            enroll_level=json_data.get("enroll_level", None),
                            puid=api_response.get("puid", None),
                            guid=api_response.get("guid", None),
                            token=api_response.get("token", None),
                            score=api_response.get("score", None),
                            message=  "" if relax_face_validation or predicted else message                            
                            )]
                        else:                            
                            return [FaceEnrollPredictResult(
                                    status=api_response.get("status", "Something went wrong"),
                                    enroll_level=json_data.get("enroll_level", None),
                                    puid= None,
                                    guid=None,
                                    score= None,
                                    message=api_response.get("message", "Something went wrong"))]                            
                else:
                     return FaceEnrollPredictResult(
                        status=result_status,
                        enroll_level=json_data.get("enroll_level", None),
                        puid=api_response.get("puid", None),
                        guid=api_response.get("guid", None),
                        token=api_response.get("token", None),
                        score=api_response.get("score", None),
                        message=  "Ok" if relax_face_validation or predicted else message
                        )
            if config_object and json.loads(config_object.get_config_param()).get("neighbors",0)>0:
                if api_response.get("PI_list", []):
                    return [FaceEnrollPredictResult(
                        status=call_status,
                        enroll_level=json_data.get("enroll_level", None),
                        puid=person.get("puid", None),
                        guid=person.get("guid", None),
                        score=person.get("score", None),
                        message=api_response.get("message", "Something went wrong")
                    ) for person in api_response.get("PI_list", [])]
                else:
                   return [FaceEnrollPredictResult(
                        status=api_response.get("status", "Something went wrong"),
                        enroll_level=json_data.get("enroll_level", None),
                        puid= None,
                        guid=None,
                        score= None,
                        message=api_response.get("message", "Something went wrong"))]
            else:
                 return FaceEnrollPredictResult(
                    status=call_status,
                    enroll_level=json_data.get("enroll_level", None),
                    puid=api_response.get("puid", None),
                    guid=api_response.get("guid", None),
                    token=api_response.get("token", None),
                    score=api_response.get("score", None),
                    message=api_response.get("message", "")
                )
        except Exception as e:
            print(e, traceback.format_exc())
            return FaceEnrollPredictResult(message=self.message.EXCEPTION_ERROR_PREDICT)

    def delete(self, puid: str, config_object: ConfigObject = None,) -> FaceDeleteResult:
        try:
            json_response = self.face_factor_processor.delete(puid,config_object)
            if not json_response:
                return FaceDeleteResult(message=self.message.EXCEPTION_ERROR_DELETE)
            return FaceDeleteResult(
                status=json_response.get("user_delete",{}).get("status", -1),
                message=json_response.get("user_delete",{}).get("message", "Deletion Failed or User not found")
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
            return FaceEnrollPredictResult(message="Something went wrong. Couldn't process the image for Document.")



    def compare_doc_with_face(
        self,
        face_data: np.array,
        doc_data: np.array,
        config_object: ConfigObject = None,
    ) -> FaceCompareResult:
        try:
            processed_document=self._doc_scan_face(image_data=doc_data)
            if processed_document.get("doc_face",{}).get("document_data",{}).get("document_validation_status",-1)!=0:
                 if processed_document.get("doc_face",{}).get("document_data",{}).get("status_message","Unable to detect face in the document.").strip()=="":
                        return FaceCompareResult(message="Unable to detect face in the document.")
                 return FaceCompareResult(message= processed_document.get("doc_face",{}).get("document_data",{}).get("status_message","Unable to detect face in the document."))
        
            cropped_face_array = processed_document.get("doc_face",{}).get("cropped_face")
            if cropped_face_array is None:
                 return FaceCompareResult(message= "Unable to detect face in the document.")
            if cropped_face_array is not None:
            
                face_compare_json_data_all = self.face_factor_processor.compare_files(
                    face_data, processed_document.get("doc_face",{}).get("cropped_face"), config_object=config_object
                )
            else:
                return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)

            call_status = FaceCompareResult.CALL_STATUS_ERROR
            if not face_compare_json_data_all:
                return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)
            else:
                call_status = FaceCompareResult.CALL_STATUS_SUCCESS
            face_data=face_compare_json_data_all.get("face_compare",{})
            call_status=face_compare_json_data_all.get("call_status",{}).get("return_status",-1)
            if face_data.get("result", None)==1:
                return FaceCompareResult(
                    result=face_data.get("result", None),
                    distance=face_data.get("distance_min", None),
                    first_validation_result=face_data.get("a_face_validation_status", None),
                    second_validation_result=face_data.get("b_face_validation_status", None),
                    status=face_data.get("result", None),
                    message= "Same face",
                )
            elif face_data.get("result", None)==-1:
                 return FaceCompareResult(
                    result=face_data.get("result", None),
                    distance=face_data.get("distance_min", None),
                    first_validation_result=face_data.get("a_face_validation_status", None),
                    second_validation_result=face_data.get("b_face_validation_status", None),
                    status=call_status,
                    message= "Different face",
                )
            else:
                 return FaceCompareResult(
                    result=face_data.get("result", None),
                    distance=face_data.get("distance_min", None),
                    first_validation_result=face_data.get("a_face_validation_status", None),
                    second_validation_result=face_data.get("b_face_validation_status", None),
                    status=call_status,
                    message=self.message.EXCEPTION_ERROR_COMPARE,
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
            
                face_compare_json_data_all = self.face_factor_processor.compare_files(
                       image_data_1, image_data_2, config_object=config_object
                )
                call_status = FaceCompareResult.CALL_STATUS_ERROR
                if not face_compare_json_data_all:
                    return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)
                else:
                    call_status = FaceCompareResult.CALL_STATUS_SUCCESS
                face_data=face_compare_json_data_all.get("face_compare",{})
                call_status=face_compare_json_data_all.get("call_status",{}).get("return_status",-1)
                if face_data.get("result", None)==1:
                    return FaceCompareResult(
                        result=face_data.get("result", None),
                        distance=face_data.get("distance_min", None),
                        first_validation_result=face_data.get("a_face_validation_status", None),
                        second_validation_result=face_data.get("b_face_validation_status", None),
                        status=face_data.get("result", None),
                        message= "Same face",
                    )
                elif face_data.get("result", None)==-1:
                    return FaceCompareResult(
                        result=face_data.get("result", None),
                        distance=face_data.get("distance_min", None),
                        first_validation_result=face_data.get("a_face_validation_status", None),
                        second_validation_result=face_data.get("b_face_validation_status", None),
                        status=call_status,
                        message= "Different face",
                    )
                else:
                    return FaceCompareResult(
                        result=face_data.get("result", None),
                        distance=face_data.get("distance_min", None),
                        first_validation_result=face_data.get("a_face_validation_status", None),
                        second_validation_result=face_data.get("b_face_validation_status", None),
                        status=call_status,
                        message=self.message.EXCEPTION_ERROR_COMPARE,
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

            # Check if call_status indicates success
            call_status = json_data.get('call_status', {})
            if call_status.get('return_status', -1) != 0:
                return FaceValidationResult(
                    error=call_status.get('return_status', -1),
                    message=self.message.AGE_ESTIMATE_ERROR,
                )

            face_age_result_object = FaceValidationResult(
                error=call_status.get('return_status', -1), message="OK"
            )

            # Get the list of faces from the 'ages' key
            ages_list = json_data.get('ages', {}).get('ages', [])
            for face_data in ages_list:
                # Get face validation data
                face_validation = face_data.get('face_validation', {})
                _return_code = face_validation.get('face_validation_status', -1)
                _bounding_box = face_validation.get('bounding_box', {})
                _top_left = _bounding_box.get('top_left', None)
                _bottom_right = _bounding_box.get('bottom_right', None)
                _age = face_data.get('estimated_age', -1.0)
                _age_confidence_score = face_data.get('age_confidence_score', 0.0)

                if _return_code in FaceValidationCode:
                    _message = FaceValidationCode(_return_code).name
                else:
                    _message = "Unknown status code"

                face_age_result_object.append_face_objects(
                    return_code=_return_code,
                    age=_age,
                    message=_message,
                    top_left_coordinate=_top_left,
                    bottom_right_coordinate=_bottom_right,
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
   
    def antispoof_check(self, image_data: np.array, config_object: Optional[ConfigObject] = None) -> AntispoofCheckResult:
            try:
                # Call the processor to check for antispoofing
                json_data = self.face_factor_processor.antispoof_check(image_data, config_object=config_object)

                # Validate response
                if json_data is None:
                    return AntispoofCheckResult(status=-100, message="No response from antispoofing processor.", is_antispoof=False)

                # Check if there is an error in processing
                if json_data.get("call_status", {}).get("return_status",0) != 0:
                    error_message = json_data.get("call_status", {}).get("return_message", "Error during antispoofing check.")
                    return AntispoofCheckResult(status=json_data.get("call_status", {}).get("return_status"), message=error_message, is_antispoof=False)
                
                if json_data.get("antispoofing", 0) in [-1,-2,-3,-4,-5,-6,-100]:
                    return AntispoofCheckResult(status=json_data.get("antispoofing", 0), message=self.message.APP_MESSAGES.get(json_data.get("antispoofing", 0), "Error during antispoofing check."), is_antispoof=False)
                # Check antispoofing result
                is_spoof_detected = json_data.get("antispoofing", 0) == 1
                return AntispoofCheckResult(status=0, message="No spoofing detected." if not is_spoof_detected else "Spoofing detected.", is_antispoof=is_spoof_detected)

            except Exception as e:
                print("Exception occurred:", e, traceback.format_exc())
                return AntispoofCheckResult(status=-100, message="Exception occurred during antispoofing check.", is_antispoof=False)
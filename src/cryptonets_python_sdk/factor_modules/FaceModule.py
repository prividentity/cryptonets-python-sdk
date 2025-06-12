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
from ..settings.configuration import ConfigObject, PARAMETERS
from ..settings.loggingLevel import LoggingLevel


class Face(metaclass=Singleton):
    def __init__(
        self,
        api_key: str,
        server_url: str,
        logging_level: LoggingLevel,        
        config_object: ConfigObject = None,
    ):
        self.message = Message()
        self.face_factor_processor = NativeMethods(
            api_key=api_key,
            server_url=server_url,
            logging_level=logging_level,            
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
            
            c_response=json_data.get("enroll_onefa", {})
            api_response=c_response.get("api_response", {})
            face_validation_data=c_response.get("face_validation_data", {})
            result =  FaceEnrollPredictResult(
                status=call_status,
                enroll_level=json_data.get("enroll_level", None),
                puid=api_response.get("puid", None),
                guid=api_response.get("guid", None),                
                score=api_response.get("score", None),
                message=self.message.get_message(int(face_validation_data.get("face_validation_status",0)))
            )
            result.api_message=api_response.get("message", None)
            result.api_status=api_response.get("status",None)
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
            res_enroll_level = json_data.get("enroll_level", None)     
            api_puid=api_response.get("puid", None)
            api_guid=api_response.get("guid", None)
            res_api_status=api_response.get("status", None)
            res_api_message=api_response.get("message", None)            
            api_score=api_response.get("score", None)
            
            predicted = res_api_status == 0 and self._valid_uuid(api_puid) and self._valid_uuid(api_guid)           
            result_status =  0 if relax_face_validation or predicted else face_validation_data.get("face_validation_status",0)
            if face_validation_data.get("face_validation_status",0)!=0:
                if config_object and json.loads(config_object.get_config_param()).get("neighbors",0)>0:
                        if api_response.get("PI_list", []):
                            return [FaceEnrollPredictResult(
                            status=face_validation_data.get("face_validation_status",0),
                            enroll_level=res_enroll_level,
                            puid=api_puid,
                            guid=api_guid,
                            score=api_score,
                            api_status=res_api_status,
                            api_message=res_api_message,
                            message=  "" if relax_face_validation or predicted else message                            
                            )]
                        else:                            
                            return [FaceEnrollPredictResult(
                                    status=api_response.get("status", FaceEnrollPredictResult.CALL_STATUS_ERROR),
                                    enroll_level=res_enroll_level,
                                    puid= None,
                                    guid=None,
                                    score= None,
                                    api_status=res_api_status,
                                    api_message=res_api_message,
                                    message=api_response.get("message", "Something went wrong"))]                            
                else:
                     return FaceEnrollPredictResult(
                        status=result_status,
                        enroll_level=res_enroll_level,
                        puid=api_puid,
                        guid=api_guid,
                        score=api_score,
                        api_status=res_api_status,
                        api_message=res_api_message,
                        message=  "Ok" if relax_face_validation or predicted else message
                        )
            if config_object and json.loads(config_object.get_config_param()).get("neighbors",0)>0:
                if api_response.get("PI_list", []):
                    return [FaceEnrollPredictResult(
                        status=call_status,
                        enroll_level=res_enroll_level,
                        puid=person.get("puid", None),
                        guid=person.get("guid", None),
                        score=person.get("score", None),
                        message=api_response.get("message", "Something went wrong")                        
                    ) for person in api_response.get("PI_list", [])]
                else:
                   return [FaceEnrollPredictResult(
                        status=api_response.get("status", "Something went wrong"),
                        enroll_level=res_enroll_level,
                        puid= None,
                        guid=None,
                        score= None,
                        api_status=res_api_status,
                        api_message=res_api_message,
                        message=api_response.get("message", "Something went wrong"))]
            else:
                 return FaceEnrollPredictResult(
                    status=call_status,
                    enroll_level=res_enroll_level,
                    puid=api_puid,
                    guid=api_guid,
                    score=api_score,
                    message=res_api_message,
                    api_status=res_api_status,
                    api_message=res_api_message
                    
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
            # process the document 
            processed_document=self._doc_scan_face(image_data=doc_data)
            if not processed_document:
                return FaceCompareResult(message="Unable to detect face in the document.")
            
            doc_validation_status=processed_document.get("doc_face",{}).get("document_data",{}).get("document_validation_status",-1)
            if doc_validation_status != 0:
                 error_message = processed_document.get("doc_face",{}).get("document_data",{}).get("status_message","Unable to detect face in the document.").strip()
                 if error_message == "": 
                    error_message = "Unable to detect face in the document."
                 return FaceCompareResult(message=error_message)
                 
            # process the image data
            cropped_face_array = processed_document.get("doc_face",{}).get("cropped_face")
            if cropped_face_array is None:
                 return FaceCompareResult(message= "Unable to detect face in the document.")
            
            return self.compare(
                image_data_1=face_data,
                image_data_2=cropped_face_array,
                config_object=config_object,
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

            call_status=face_compare_json_data_all.get("call_status",{}).get("return_status",None)
            if (call_status == None):
                    return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)
            
            if call_status != 0:
                error_message = face_compare_json_data_all.get("call_status", {}).get("return_message", self.message.EXCEPTION_ERROR_COMPARE)
                return FaceCompareResult(status=FaceCompareResult.CALL_STATUS_ERROR, message=error_message)
            
            face_data=face_compare_json_data_all.get("face_compare",{})
            if face_data is None:
                return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)

            result = face_data.get("result", None)
            if result is None:
                return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)
            
            if result == 1:
                returned_message = "Same face"
            elif result == -1:
                returned_message = "Different face"
            else:
                return FaceCompareResult(message=self.message.EXCEPTION_ERROR_COMPARE)

            return FaceCompareResult(
                result=result,                
                distance=face_data.get("distance_mean", None),                
                first_validation_result=face_data.get("a_face_validation_status", None),
                second_validation_result=face_data.get("b_face_validation_status", None),
                status=call_status,
                message= returned_message
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
                    _message = self.message.get_message(_return_code,False)
                else:
                    _message = "Unknown status code"

                face_age_result_object.append_face_objects(
                    return_code=_return_code,
                    age=_age,
                    message=_message,
                    top_left_coordinate=_top_left,
                    bottom_right_coordinate=_bottom_right,
                    age_confidence_score=_age_confidence_score 
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
            
            face_iso_data=json_data.get("face_iso",{})
            call_status=json_data.get("call_status",{}).get("return_status",-1)

            if call_status != 0:
                error_message = json_data.get("call_status", {}).get("return_message", self.message.EXCEPTION_ERROR_GET_ISO_FACE)
                return ISOFaceResult(status=call_status, message=error_message)            
            
            returned_status = face_iso_data.get("face_validation_data",{}).get("face_validation_status", -1)
            score = face_iso_data.get("face_validation_data",{}).get("face_confidence_score", -1)
            if returned_status != 0:
               returned_message = Message.APP_MESSAGES.get(returned_status, "Unknown status code")  
            else:
               returned_message = "OK"
           
            return ISOFaceResult(
                iso_image_width=json_data.get("iso_image_width", None),
                iso_image_height=json_data.get("iso_image_height", None),
                iso_image_channels=json_data.get("iso_image_channels", None),
                confidence=score,
                image=json_data.get("image", None),
                status=returned_status,
                message=returned_message,
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
                    return AntispoofCheckResult(status=-100, message="No response from antispoofing processor.", is_spoof=False)

                # Check if there is an error in processing
                if json_data.get("call_status", {}).get("return_status",0) != 0:
                    error_message = json_data.get("call_status", {}).get("return_message", "Error during antispoofing check.")
                    return AntispoofCheckResult(status=json_data.get("call_status", {}).get("return_status"), message=error_message, is_spoof=False)
                
                if json_data.get("antispoofing", 0) in [-1,-2,-3,-4,-5,-6,-100]:
                    return AntispoofCheckResult(status=json_data.get("antispoofing", 0), message=self.message.APP_MESSAGES.get(json_data.get("antispoofing", 0), "Error during antispoofing check."), is_spoof=False)
                # Check antispoofing result
                is_spoof_detected = json_data.get("antispoofing", 0) == 1
                return AntispoofCheckResult(status=0, message="No spoofing detected." if not is_spoof_detected else "Spoofing detected.", is_spoof=is_spoof_detected)

            except Exception as e:
                print("Exception occurred:", e, traceback.format_exc())
                return AntispoofCheckResult(status=-100, message="Exception occurred during antispoofing check.", is_spoof=False)
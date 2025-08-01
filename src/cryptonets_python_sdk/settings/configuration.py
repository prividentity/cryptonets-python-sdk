import json
import sys
from enum import Enum, EnumMeta
from typing import Dict


class __PARAMETERSMETA(EnumMeta):
    def __contains__(cls, item):
        return item in [v for v in cls.__members__.values()]


class PARAMETERS(str, Enum, metaclass=__PARAMETERSMETA):
    """PARAMETERS contains the valid key values for configuring additional parameters in the factor processor.
    """

    INPUT_IMAGE_FORMAT = "input_image_format"
    CONTEXT_STRING = "context_string"
    FACE_THRESHOLDS_REM_BAD_EMB = "face_thresholds_rem_bad_emb"
    BLUR_THRESHOLD_ENROLL_PRED = "blur_threshold_enroll_pred"
    THRESHOLD_PROFILE_ENROLL = "threshold_profile_enroll"
    THRESHOLD_PROFILE_PREDICT = "threshold_profile_predict"
    THRESHOLD_USER_RIGHT = "threshold_user_right"
    THRESHOLD_USER_LEFT = "threshold_user_left"
    THRESHOLD_USER_TOO_FAR = "threshold_user_too_far"
    THRESHOLD_USER_TOO_CLOSE = "threshold_user_too_close"
    CONF_SCORE_THR_ENROLL = "conf_score_thr_enroll"
    CONF_SCORE_THR_PREDICT = "conf_score_thr_predict"
    MIN_DOCUMENT_BORDER = "min_document_border"
    DISALLOWED_RESULTS = "disallowed_results" # for internal usage
    ALLOWED_RESULTS = "allowed_results" # for internal usage
    ORIENTATION_ID_VALUE = "orientation_id_value"
    SEND_ORIGINAL_IMAGES = "send_original_images"
    COLLECTION_NAME = "collection_name"
    USER_IDENTIFIER="identifier"
    K="neighbors"
    FACE_THRESHOLD="face_thresholds_med"
    DOC_SCAN_FACE_DOC_VALIDATIONS_OFF="doc_scan_face_doc_validations_off"
    THRESHOLD_HIGH_VERTICAL="threshold_high_vertical_enroll"    
    DOCUMENT_AUTO_ROTATION = "document_auto_rotation"
    ESTIMATE_AGE_FACE_VALIDATIONS_OFF = "estimate_age_face_validations_off",
    RELAX_FACE_VALIDATION = "relax_face_validation"
    # use only for age predict
    USE_AGE_ESTIMATION_WITH_MODEL_STDD ="use_age_estimate_with_model_stdd"
    DISABLE_AGE_ESTIMATION_ANTISPOOF = "skip_antispoof",
    CONSIDER_BIGGEST_FACE = "consider_biggest_face",
    SINGLE_FACE_VALIDATION_RESULT = "single_face_validation_result" 
    SINGLE_FACE_AGE_RESULT = "single_face_age_result" 
    AGE_FACE_LANDMARK_MODEL_ID = "age_face_landmarks_model_id"
    THRESHOLD_DOWN_VERTICAL="threshold_down_vertical_enroll"
    THRESHOLD_FACE_DOWN="threshold_user_down"
    THRESHOLD_FACE_UP="threshold_user_up"




class ParameterValidator:
    def __init__(self):
        self.__parameter = {}
        self.__populate_parameters()
        

    def __populate_parameters(self):
        self.__parameter[PARAMETERS.INPUT_IMAGE_FORMAT] = self.Parameter(
            name=PARAMETERS.INPUT_IMAGE_FORMAT,
            _type="SET",
            valid_set=["rgb", "rgba", "bgr"],
        )
        self.__parameter[PARAMETERS.CONTEXT_STRING] = self.Parameter(
            name=PARAMETERS.CONTEXT_STRING, _type="SET", valid_set=["enroll", "predict"]
        )
        self.__parameter[PARAMETERS.FACE_THRESHOLDS_REM_BAD_EMB] = self.Parameter(
            name=PARAMETERS.FACE_THRESHOLDS_REM_BAD_EMB,
            _type="NUMBER",
            min_value=0,
            max_value=2,
        )
        self.__parameter[PARAMETERS.FACE_THRESHOLD] = self.Parameter(
            name=PARAMETERS.FACE_THRESHOLD,
            _type="NUMBER",
            min_value=0,
            max_value=2,
        )
        self.__parameter[PARAMETERS.BLUR_THRESHOLD_ENROLL_PRED] = self.Parameter(
            name=PARAMETERS.BLUR_THRESHOLD_ENROLL_PRED,
            _type="NUMBER",
            min_value=0,
            max_value=10000,
        )
        self.__parameter[PARAMETERS.THRESHOLD_PROFILE_ENROLL] = self.Parameter(
            name=PARAMETERS.THRESHOLD_PROFILE_ENROLL,
            _type="NUMBER",
            min_value=-0.1,
            max_value=2,
        )
        self.__parameter[PARAMETERS.THRESHOLD_PROFILE_PREDICT] = self.Parameter(
            name=PARAMETERS.THRESHOLD_PROFILE_PREDICT,
            _type="NUMBER",
            min_value=-0.1,
            max_value=2,
        )
        self.__parameter[PARAMETERS.THRESHOLD_USER_RIGHT] = self.Parameter(
            name=PARAMETERS.THRESHOLD_USER_RIGHT,
            _type="NUMBER",
            min_value=-0.1,
            max_value=2,
        )
        self.__parameter[PARAMETERS.THRESHOLD_USER_LEFT] = self.Parameter(
            name=PARAMETERS.THRESHOLD_USER_LEFT,
            _type="NUMBER",
            min_value=-0.1,
            max_value=2,
        )
        self.__parameter[PARAMETERS.THRESHOLD_USER_TOO_FAR] = self.Parameter(
            name=PARAMETERS.THRESHOLD_USER_TOO_FAR,
            _type="NUMBER",
            min_value=-0.1,
            max_value=2,
        )
        self.__parameter[PARAMETERS.THRESHOLD_USER_TOO_CLOSE] = self.Parameter(
            name=PARAMETERS.THRESHOLD_USER_TOO_CLOSE,
            _type="NUMBER",
            min_value=-0.1,
            max_value=2,
        )
        self.__parameter[PARAMETERS.CONF_SCORE_THR_ENROLL] = self.Parameter(
            name=PARAMETERS.CONF_SCORE_THR_ENROLL,
            _type="NUMBER",
            min_value=-0.1,
            max_value=2,
        )
        self.__parameter[PARAMETERS.CONF_SCORE_THR_PREDICT] = self.Parameter(
            name=PARAMETERS.CONF_SCORE_THR_PREDICT,
            _type="NUMBER",
            min_value=-0.1,
            max_value=2,
        )
        self.__parameter[PARAMETERS.MIN_DOCUMENT_BORDER] = self.Parameter(
            name=PARAMETERS.MIN_DOCUMENT_BORDER, _type="ANY"
        )
        self.__parameter[PARAMETERS.DISALLOWED_RESULTS] = self.Parameter(
            name=PARAMETERS.DISALLOWED_RESULTS, _type="ANY"
        )
        self.__parameter[PARAMETERS.ALLOWED_RESULTS] = self.Parameter(
            name=PARAMETERS.ALLOWED_RESULTS, _type="ANY"
        )
        self.__parameter[PARAMETERS.ORIENTATION_ID_VALUE] = self.Parameter(
            name=PARAMETERS.ORIENTATION_ID_VALUE, _type="ANY"
        )
        self.__parameter[PARAMETERS.SEND_ORIGINAL_IMAGES] = self.Parameter(
            name=PARAMETERS.SEND_ORIGINAL_IMAGES, _type="BOOL"
        )
        self.__parameter[PARAMETERS.USER_IDENTIFIER] = self.Parameter(
            name=PARAMETERS.USER_IDENTIFIER, _type="ANY"
        )

        self.__parameter[PARAMETERS.DOC_SCAN_FACE_DOC_VALIDATIONS_OFF] = self.Parameter(
            name=PARAMETERS.DOC_SCAN_FACE_DOC_VALIDATIONS_OFF, _type="BOOL")
        
        self.__parameter[PARAMETERS.ESTIMATE_AGE_FACE_VALIDATIONS_OFF] = self.Parameter(
            name=PARAMETERS.ESTIMATE_AGE_FACE_VALIDATIONS_OFF, _type="BOOL")        
        
        self.__parameter[PARAMETERS.THRESHOLD_HIGH_VERTICAL] = self.Parameter(
            name=PARAMETERS.THRESHOLD_HIGH_VERTICAL,
            _type="NUMBER",
            min_value=-100,
            max_value=100,
        )        

        self.__parameter[PARAMETERS.COLLECTION_NAME] = self.Parameter(
            name=PARAMETERS.COLLECTION_NAME, _type="ANY")

        self.__parameter[PARAMETERS.K] = self.Parameter(
            name=PARAMETERS.K,_type="NUMBER", min_value=1, max_value=100)

        self.__parameter[PARAMETERS.DOCUMENT_AUTO_ROTATION] = self.Parameter(
            name=PARAMETERS.DOCUMENT_AUTO_ROTATION,_type="BOOL")
        
        self.__parameter[PARAMETERS.ESTIMATE_AGE_FACE_VALIDATIONS_OFF] = self.Parameter(
            name=PARAMETERS.ESTIMATE_AGE_FACE_VALIDATIONS_OFF,_type="BOOL")

        # This should not be included in the config and remove before passing
        # it to the operation
        self.__parameter[PARAMETERS.RELAX_FACE_VALIDATION] = self.Parameter(
            name=PARAMETERS.RELAX_FACE_VALIDATION,_type="BOOL")

        # This should not be included in the config and remove before passing
        # it to the operation
        self.__parameter[PARAMETERS.RELAX_FACE_VALIDATION] = self.Parameter(
            name=PARAMETERS.RELAX_FACE_VALIDATION, _type="BOOL")

        self.__parameter[PARAMETERS.USE_AGE_ESTIMATION_WITH_MODEL_STDD] = self.Parameter(
            name=PARAMETERS.USE_AGE_ESTIMATION_WITH_MODEL_STDD, _type="BOOL")
        
        self.__parameter[PARAMETERS.DISABLE_AGE_ESTIMATION_ANTISPOOF] = self.Parameter(
            name=PARAMETERS.DISABLE_AGE_ESTIMATION_ANTISPOOF, _type="BOOL")
        
        self.__parameter[PARAMETERS.CONSIDER_BIGGEST_FACE] = self.Parameter(
            name=PARAMETERS.CONSIDER_BIGGEST_FACE, _type="BOOL")
        
        self.__parameter[PARAMETERS.SINGLE_FACE_VALIDATION_RESULT] = self.Parameter(
            name=PARAMETERS.SINGLE_FACE_VALIDATION_RESULT, _type="BOOL",
        )

        self.__parameter[PARAMETERS.SINGLE_FACE_AGE_RESULT] = self.Parameter(
            name=PARAMETERS.SINGLE_FACE_AGE_RESULT, _type="BOOL",
        )

        self.__parameter[PARAMETERS.AGE_FACE_LANDMARK_MODEL_ID] = self.Parameter(
            name=PARAMETERS.AGE_FACE_LANDMARK_MODEL_ID, 
            _type="NUMBER",
            min_value=0,
            max_value=1000,
        )

        self.__parameter[PARAMETERS.THRESHOLD_DOWN_VERTICAL] = self.Parameter(
            name=PARAMETERS.THRESHOLD_DOWN_VERTICAL,
            _type="NUMBER",
            min_value=-100,
            max_value=100,
        ) 
        
        self.__parameter[PARAMETERS.THRESHOLD_FACE_DOWN] = self.Parameter(
            name=PARAMETERS.THRESHOLD_FACE_DOWN,
            _type="NUMBER",
            min_value=-100,
            max_value=100,
        ) 

        self.__parameter[PARAMETERS.THRESHOLD_FACE_UP] = self.Parameter(
            name=PARAMETERS.THRESHOLD_FACE_UP,
            _type="NUMBER",
            min_value=-100,
            max_value=100,
        )     


    def validate(self, key, value):
        return self.__parameter[key].validate(value)

    class Parameter:
        def __init__(
            self, name=None, _type=None, min_value=None, max_value=None, valid_set=None
        ):
            self.__name = name
            # ANY, BOOL, SET, NUMBER
            self.__type = _type
            self.__min_value = min_value
            self.__max_value = max_value
            self.__valid_set = valid_set

        def validate(self, value):
            if self.__type == "ANY":
                return True
            if self.__type == "BOOL":
                if value in [False, "True", "true", "false", "False", True]:
                    return True
                return False

            if self.__type == "SET":
                if value in self.__valid_set:
                    return True
                return False

            if self.__type == "NUMBER":
                if (
                    isinstance(value, (int, float))
                    and self.__min_value <= value <= self.__max_value
                ):
                    return True
                return False

            return False



class FACE_VALIDATION_STATUSES   (Enum):
        FV_OK = 0                    # Face validation is successful.
        FV_ERR = -100                # Error occurred during face validation.
        FV_MANY_FACES_DETECTED = -2  # Too many faces detected in the image.
        FV_FACE_NOT_DETECTED = -1    # Face not detected in the image.
        FV_FACE_TOO_CLOSE = 3        # Face is too close to the camera.
        FV_FACE_TOO_FAR = 4          # Face is too far from the camera.
        FV_FACE_RIGHT = 5            # Face is turned to the right.
        FV_FACE_LEFT = 6             # Face is turned to the left.
        FV_FACE_UP = 7               # Face is turned upwards.
        FV_FACE_DOWN = 8             # Face is turned downwards.
        FV_IMAGE_BLURR = 9           # Image is blurred.
        FV_FACE_WITH_GLASS = 10      # Face is wearing glasses.
        FV_FACE_WITH_MASK = 11       # Face is wearing a mask.
        FV_LOOKING_LEFT = 12         # Face is looking to the left.
        FV_LOOKING_RIGHT = 13        # Face is looking to the right.
        FV_LOOKING_HIGH = 14         # Face is looking upwards.
        FV_LOOKING_DOWN = 15         # Face is looking downwards.
        FV_FACE_TOO_DARK = 16        # Face is too dark.
        FV_FACE_TOO_BRIGHT = 17      # Face is too bright.
        FV_FACE_LOW_VAL_CONF = 18    # Low confidence in face validation.
        FV_INVALID_FACE_BACKGROUND = 19   # Invalid face background.
        FV_EYE_BLINK = 20            # Eye blink detected.
        FV_MOUTH_OPENED = 21         # Mouth opened detected.
        FV_FACE_ROTATED_RIGHT = 22   # Face is rotated to the right.
        FV_FACE_ROTATED_LEFT = 23    # Face is rotated to the left.
        FV_FACE_WITH_EYEGLASSES_AND_FACEMASK = 24  # The face is wearing eyeglasses and a face mask at the same time.
        FV_FACE_NOT_IN_OVAL = 25     # The face is not in the anti-spoof recommended position (target oval).    


class ANTISPOOFING_STATUSES   (Enum):
  AS_NO_SPOOF_DETECTED = 0  # No spoofing detected.
  AS_SPOOF_DETECTED = 1 # Spoofing detected in the image.
  AS_GENERIC_ERROR = -100 # Generic error occurred.
  AS_NOT_PERFORMED = -6 # Anti-spoofing not performed.

class ConfigObject:
    """Configuration Object class handles the parameters that are required to initialize the server with
    other fine controlling variables for factor processor.

    Parameters
    ----------
    config_param : Dict[PARAMETERS, str]
        Configuration parameters for changing the behaviour of face processing.
        Refer PARAMETERS class for valid values

    Returns
    -------
    ConfigObject
        Instance of the ConfigObject class.
    """

    def __init__(self, config_param: Dict[PARAMETERS, str] = None):
        if config_param is None:
            self._config_param = {}
        else:
            self._config_param = config_param
        self._validate_parameter = ParameterValidator()
        self.parse_config()

    def parse_config(self):
        try:
            for key, value in self._config_param.items():
                if key not in PARAMETERS:
                    raise ValueError(
                        "Invalid key '{}' in config parameters".format(key)
                    )

                if not self._validate_parameter.validate(key, value):
                    raise ValueError(
                        "Invalid key value pair\n'{}' : '{}'".format(key, value)
                    )
        except Exception as exp:
            print("Config Error:", exp)
            sys.exit(1)

    def _get_param_value(self, key: PARAMETERS) -> str | None:
        return self._config_param.get(key) 

    def get_config_param(self):
        if len(self._config_param) == 0:
            return None
        self._config_param.pop(PARAMETERS.USE_AGE_ESTIMATION_WITH_MODEL_STDD, None)
        config_param_dict = {}
        for key, value in self._config_param.items():
            config_param_dict[key.value] = value

        if len(config_param_dict) == 0:
            return None
        if PARAMETERS.RELAX_FACE_VALIDATION in config_param_dict:
            relax_face_validation = config_param_dict[PARAMETERS.RELAX_FACE_VALIDATION]
            if relax_face_validation not in [True, False]:
                raise ValueError(
                    "Invalid key value pair\n'{}' : '{}'".format(
                        PARAMETERS.RELAX_FACE_VALIDATION, relax_face_validation
                    )
                )
            else: 
                # if relax is true then allow all face validation statuses
                if relax_face_validation == True: 
                    config_param_dict[PARAMETERS.ALLOWED_RESULTS] = [
                        FACE_VALIDATION_STATUSES.FV_FACE_TOO_CLOSE.value,        # Face is too close to the camera.
                        FACE_VALIDATION_STATUSES.FV_FACE_TOO_FAR.value,          # Face is too far from the camera.
                        FACE_VALIDATION_STATUSES.FV_FACE_RIGHT.value,            # Face is turned to the right.
                        FACE_VALIDATION_STATUSES.FV_FACE_LEFT.value,             # Face is turned to the left.
                        FACE_VALIDATION_STATUSES.FV_FACE_UP.value,               # Face is turned upwards.
                        FACE_VALIDATION_STATUSES.FV_FACE_DOWN.value,             # Face is turned downwards.
                        FACE_VALIDATION_STATUSES.FV_IMAGE_BLURR.value,           # Image is blurred.
                        FACE_VALIDATION_STATUSES.FV_FACE_WITH_GLASS.value,      # Face is wearing glasses.
                        FACE_VALIDATION_STATUSES.FV_FACE_WITH_MASK.value,       # Face is wearing a mask.
                        FACE_VALIDATION_STATUSES.FV_LOOKING_LEFT.value,         # Face is looking to the left.
                        FACE_VALIDATION_STATUSES.FV_LOOKING_RIGHT.value,        # Face is looking to the right.
                        FACE_VALIDATION_STATUSES.FV_LOOKING_HIGH.value,         # Face is looking upwards.
                        FACE_VALIDATION_STATUSES.FV_LOOKING_DOWN.value,         # Face is looking downwards.
                        FACE_VALIDATION_STATUSES.FV_FACE_TOO_DARK.value,        # Face is too dark.
                        FACE_VALIDATION_STATUSES.FV_FACE_TOO_BRIGHT.value,      # Face is too bright.
                        FACE_VALIDATION_STATUSES.FV_FACE_LOW_VAL_CONF.value,    # Low confidence in face validation.
                        FACE_VALIDATION_STATUSES.FV_INVALID_FACE_BACKGROUND.value,   # Invalid face background.
                        FACE_VALIDATION_STATUSES.FV_EYE_BLINK.value,            # Eye blink detected.
                        FACE_VALIDATION_STATUSES.FV_MOUTH_OPENED.value,         # Mouth opened detected.
                        FACE_VALIDATION_STATUSES.FV_FACE_ROTATED_RIGHT.value,   # Face is rotated to the right.
                        FACE_VALIDATION_STATUSES.FV_FACE_ROTATED_LEFT.value,    # Face is rotated to the left.
                        FACE_VALIDATION_STATUSES.FV_FACE_WITH_EYEGLASSES_AND_FACEMASK.value,  # The face is wearing eyeglasses and a face mask at the same time.
                        FACE_VALIDATION_STATUSES.FV_FACE_NOT_IN_OVAL.value     # The face is not in the anti-spoof recommended position (target oval).    
                    ]

            # remove the key as t is not a native configuration key
            config_param_dict.pop(PARAMETERS.RELAX_FACE_VALIDATION)  
            
        return json.dumps(config_param_dict)
    

    def __str__(self):
        config_string = ""
        for key, value in self._config_param.items():
            config_string += "{}\t{}\n".format(key, value)
        return "\nPARAMETERS\n{}\n{}".format("-" * 10, config_string)

    @property
    def config_param(self) -> Dict[PARAMETERS, str]:
        """
        Returns the configuration parameter
        """
        return self._config_param

    @config_param.setter
    def config_param(self, value):
        self._config_param = value

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
    CONF_FAST_PROCESS = "conf_fast_process"
    INPUT_TYPE = "input_type"
    FACE_THRESHOLDS_REM_BAD_EMB = "face_thresholds_rem_bad_emb"
    BLUR_THRESHOLD_DOC_LEVEL_1 = "blur_threshold_doc_level_1"
    BLUR_THRESHOLD_DOC_LEVEL_2 = "blur_threshold_doc_level_2"
    BLUR_THRESHOLD_ENROLL_PRED = "blur_threshold_enroll_pred"
    THRESHOLD_PROFILE_ENROLL = "threshold_profile_enroll"
    THRESHOLD_PROFILE_PREDICT = "threshold_profile_predict"
    THRESHOLD_VERTICAL_ENROLL = "threshold_vertical_enroll"
    THRESHOLD_VERTICAL_PREDICT = "threshold_vertical_predict"
    THRESHOLD_USER_RIGHT = "threshold_user_right"
    THRESHOLD_USER_LEFT = "threshold_user_left"
    THRESHOLD_USER_TOO_FAR = "threshold_user_too_far"
    THRESHOLD_USER_TOO_CLOSE = "threshold_user_too_close"
    IMAGE_BORDER = "image_border"
    IMAGE_PRE_PROC = "image_pre_proc"
    THRESHOLD_GLASS = "threshold_glass"
    THRESHOLD_MASK = "threshold_mask"
    FACE_THRESHOLD_RIGHT = "face_threshold_right"
    FACE_THRESHOLD_LEFT = "face_threshold_left"
    FACE_THRESHOLD_VERTICAL = "face_threshold_vertical"
    CONF_SCORE_THR_ENROLL = "conf_score_thr_enroll"
    CONF_SCORE_THR_PREDICT = "conf_score_thr_predict"
    MIN_DOCUMENT_BORDER = "min_document_border"
    DISALLOWED_RESULTS = "disallowed_results"
    ALLOWED_RESULTS = "allowed_results"
    DOCUMENT_FACE_CHECK_VALIDITY = "document_face_check_validity"
    DOCUMENT_CHECK_VALIDITY = "document_check_validity"
    DOCUMENT_FACE_PREDICT = "document_face_predict"
    ENABLE_DOC_PERSPECTIVE_CORRECTION = "enable_doc_perspective_correction"
    ENROLL_ALLOW_EYE_GLASS = "enroll_allow_eye_glass"
    ORIENTATION_ID_VALUE = "orientation_id_value"
    FACE_DETECT_PREFERRED_SIZE = "face_detect_preferred_size"
    FACE_DETECT_MAX_OUT_IMAGE_SIZE = "face_detect_max_out_image_size"
    SEND_ORIGINAL_IMAGES = "send_original_images"


class ParameterValidator:
    def __init__(self):
        self.__parameter = {}
        self.__populate_parameters()

    def __populate_parameters(self):
        self.__parameter[PARAMETERS.INPUT_IMAGE_FORMAT] = self.Parameter(
            name=PARAMETERS.INPUT_IMAGE_FORMAT, _type="SET", valid_set=["rgb", "rgba", "bgr"])
        self.__parameter[PARAMETERS.CONTEXT_STRING] = self.Parameter(name=PARAMETERS.CONTEXT_STRING,
                                                                     _type="SET",
                                                                     valid_set=["enroll", "predict"])
        self.__parameter[PARAMETERS.CONF_FAST_PROCESS] = self.Parameter(name=PARAMETERS.CONF_FAST_PROCESS,
                                                                        _type="BOOL")
        self.__parameter[PARAMETERS.INPUT_TYPE] = self.Parameter(name=PARAMETERS.INPUT_TYPE, _type="SET",
                                                                 valid_set=["face", "document-id",
                                                                            "document-barcode"])
        self.__parameter[PARAMETERS.FACE_THRESHOLDS_REM_BAD_EMB] = self.Parameter(
            name=PARAMETERS.FACE_THRESHOLDS_REM_BAD_EMB, _type="NUMBER", min_value=0, max_value=2)
        self.__parameter[PARAMETERS.BLUR_THRESHOLD_DOC_LEVEL_1] = self.Parameter(
            name=PARAMETERS.BLUR_THRESHOLD_DOC_LEVEL_1, _type="NUMBER", min_value=0, max_value=10000)
        self.__parameter[PARAMETERS.BLUR_THRESHOLD_DOC_LEVEL_2] = self.Parameter(
            name=PARAMETERS.BLUR_THRESHOLD_DOC_LEVEL_2, _type="NUMBER", min_value=0, max_value=10000)
        self.__parameter[PARAMETERS.BLUR_THRESHOLD_ENROLL_PRED] = self.Parameter(
            name=PARAMETERS.BLUR_THRESHOLD_ENROLL_PRED, _type="NUMBER", min_value=0, max_value=10000)
        self.__parameter[PARAMETERS.THRESHOLD_PROFILE_ENROLL] = self.Parameter(
            name=PARAMETERS.THRESHOLD_PROFILE_ENROLL, _type="NUMBER", min_value=-0.1, max_value=2)
        self.__parameter[PARAMETERS.THRESHOLD_PROFILE_PREDICT] = self.Parameter(
            name=PARAMETERS.THRESHOLD_PROFILE_PREDICT, _type="NUMBER", min_value=-0.1, max_value=2)
        self.__parameter[PARAMETERS.THRESHOLD_VERTICAL_ENROLL] = self.Parameter(
            name=PARAMETERS.THRESHOLD_VERTICAL_ENROLL, _type="NUMBER", min_value=-0.1, max_value=2)
        self.__parameter[PARAMETERS.THRESHOLD_VERTICAL_PREDICT] = self.Parameter(
            name=PARAMETERS.THRESHOLD_VERTICAL_PREDICT, _type="NUMBER", min_value=-0.1, max_value=2)
        self.__parameter[PARAMETERS.THRESHOLD_USER_RIGHT] = self.Parameter(
            name=PARAMETERS.THRESHOLD_USER_RIGHT, _type="NUMBER", min_value=-0.1, max_value=2)
        self.__parameter[PARAMETERS.THRESHOLD_USER_LEFT] = self.Parameter(
            name=PARAMETERS.THRESHOLD_USER_LEFT, _type="NUMBER", min_value=-0.1, max_value=2)
        self.__parameter[PARAMETERS.THRESHOLD_USER_TOO_FAR] = self.Parameter(
            name=PARAMETERS.THRESHOLD_USER_TOO_FAR, _type="NUMBER", min_value=-0.1, max_value=2)
        self.__parameter[PARAMETERS.THRESHOLD_USER_TOO_CLOSE] = self.Parameter(
            name=PARAMETERS.THRESHOLD_USER_TOO_CLOSE, _type="NUMBER", min_value=-0.1, max_value=2)
        self.__parameter[PARAMETERS.IMAGE_BORDER] = self.Parameter(name=PARAMETERS.IMAGE_BORDER,
                                                                   _type="NUMBER", min_value=0, max_value=0.1)
        self.__parameter[PARAMETERS.IMAGE_PRE_PROC] = self.Parameter(name=PARAMETERS.IMAGE_PRE_PROC,
                                                                     _type="SET",
                                                                     valid_set=["zoom_pan", "rotate90",
                                                                                "rotate180", "rotate270", "blur",
                                                                                "fliplr", "none"])
        self.__parameter[PARAMETERS.THRESHOLD_GLASS] = self.Parameter(name=PARAMETERS.THRESHOLD_GLASS,
                                                                      _type="NUMBER", min_value=-0.1,
                                                                      max_value=2)
        self.__parameter[PARAMETERS.THRESHOLD_MASK] = self.Parameter(name=PARAMETERS.THRESHOLD_MASK,
                                                                     _type="NUMBER", min_value=-0.1, max_value=2)
        self.__parameter[PARAMETERS.FACE_THRESHOLD_RIGHT] = self.Parameter(
            name=PARAMETERS.FACE_THRESHOLD_RIGHT, _type="ANY")
        self.__parameter[PARAMETERS.FACE_THRESHOLD_LEFT] = self.Parameter(
            name=PARAMETERS.FACE_THRESHOLD_LEFT, _type="ANY")
        self.__parameter[PARAMETERS.FACE_THRESHOLD_VERTICAL] = self.Parameter(
            name=PARAMETERS.FACE_THRESHOLD_VERTICAL, _type="ANY")
        self.__parameter[PARAMETERS.CONF_SCORE_THR_ENROLL] = self.Parameter(
            name=PARAMETERS.CONF_SCORE_THR_ENROLL, _type="NUMBER", min_value=-0.1, max_value=2)
        self.__parameter[PARAMETERS.CONF_SCORE_THR_PREDICT] = self.Parameter(
            name=PARAMETERS.CONF_SCORE_THR_PREDICT, _type="NUMBER", min_value=-0.1, max_value=2)
        self.__parameter[PARAMETERS.MIN_DOCUMENT_BORDER] = self.Parameter(
            name=PARAMETERS.MIN_DOCUMENT_BORDER, _type="ANY")
        self.__parameter[PARAMETERS.DISALLOWED_RESULTS] = self.Parameter(
            name=PARAMETERS.DISALLOWED_RESULTS, _type="ANY")
        self.__parameter[PARAMETERS.ALLOWED_RESULTS] = self.Parameter(name=PARAMETERS.DISALLOWED_RESULTS,
                                                                      _type="ANY")
        self.__parameter[PARAMETERS.DOCUMENT_FACE_CHECK_VALIDITY] = self.Parameter(
            name=PARAMETERS.DOCUMENT_FACE_CHECK_VALIDITY, _type="BOOL")
        self.__parameter[PARAMETERS.DOCUMENT_CHECK_VALIDITY] = self.Parameter(
            name=PARAMETERS.DOCUMENT_CHECK_VALIDITY, _type="BOOL")
        self.__parameter[PARAMETERS.DOCUMENT_FACE_PREDICT] = self.Parameter(
            name=PARAMETERS.DOCUMENT_FACE_PREDICT, _type="BOOL")
        self.__parameter[PARAMETERS.ENABLE_DOC_PERSPECTIVE_CORRECTION] = self.Parameter(
            name=PARAMETERS.ENABLE_DOC_PERSPECTIVE_CORRECTION, _type="BOOL")
        self.__parameter[PARAMETERS.ENROLL_ALLOW_EYE_GLASS] = self.Parameter(
            name=PARAMETERS.ENROLL_ALLOW_EYE_GLASS, _type="BOOL")
        self.__parameter[PARAMETERS.ORIENTATION_ID_VALUE] = self.Parameter(
            name=PARAMETERS.ORIENTATION_ID_VALUE, _type="ANY")
        self.__parameter[PARAMETERS.FACE_DETECT_PREFERRED_SIZE] = self.Parameter(
            name=PARAMETERS.FACE_DETECT_PREFERRED_SIZE, _type="ANY")
        self.__parameter[PARAMETERS.FACE_DETECT_MAX_OUT_IMAGE_SIZE] = self.Parameter(
            name=PARAMETERS.FACE_DETECT_MAX_OUT_IMAGE_SIZE, _type="ANY")
        self.__parameter[PARAMETERS.SEND_ORIGINAL_IMAGES] = self.Parameter(
            name=PARAMETERS.SEND_ORIGINAL_IMAGES, _type="BOOL")

    def validate(self, key, value):
        return self.__parameter[key].validate(value)

    class Parameter:
        def __init__(self, name=None, _type=None, min_value=None, max_value=None, valid_set=None):
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
                if isinstance(value, (int, float)) and self.__min_value <= value <= self.__max_value:
                    return True
                return False

            return False


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
                    raise ValueError("Invalid key '{}' in config parameters".format(key))

                if not self._validate_parameter.validate(key, value):
                    raise ValueError("Invalid key value pair\n'{}' : '{}'".format(key, value))
        except ValueError as exp:
            print("Config Error:", exp)
            sys.exit(1)

    def get_config_param(self):
        if len(self._config_param) == 0:
            return None
        config_param_dict = {}
        for key, value in self._config_param.items():
            config_param_dict[key.value] = value
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

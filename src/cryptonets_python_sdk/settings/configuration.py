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
    INPUT_IMAGE_FORMAT = "inputImageFormat"
    CONTEXT_STRING = "contextString"
    INPUT_TYPE = "inputType"
    CONF_SCORE_THR_ENROLL = "confScoreThrEnroll"
    CONF_SCORE_THR_PREDICT = "confScoreThrPredict"
    BLUR_THRESHOLD_ENROLL_PRED = "blurThresholdEnrollPred"
    THRESHOLD_PROFILE_ENROLL = "thresholdProfileEnroll"
    THRESHOLD_HIGH_VERTICAL_ENROLL = "threshold_high_vertical_enroll"
    THRESHOLD_DOWN_VERTICAL_ENROLL = "threshold_down_vertical_enroll"
    THRESHOLD_USER_RIGHT = "thresholdUserRight"
    THRESHOLD_USER_LEFT = "thresholdUserLeft"
    THRESHOLD_USER_TOO_FAR = "threshold_user_too_far"
    THRESHOLD_USER_TOO_CLOSE = "threshold_user_too_close"
    ANGLE_ROTATION_LEFT_THRESHOLD = "angle_rotation_left_threshold"
    ANGLE_ROTATION_RIGHT_THRESHOLD = "angle_rotation_right_threshold"
    FACE_TOO_BRIGHT = "face_too_bright"
    FACE_TOO_DARK = "face_too_dark"
    SKIP_ANTISPOOF= "skip_antispoof"
    SINGLE_FACE_AGE_RESUL= "single_face_age_resul"
    SPOOF_FILTER_THRESHOLD="spoof_filter_threshold"
    ESTIMATE_AGE_RESERVATION_CALLS="ESTIMATE_AGE_RESERVATION_CALLS"
    DOC_FRONT_RESERVATION_CALLS="DOC_FRONT_RESERVATION_CALLS"
    FACE_RESERVATION_CALLS="FACE_RESERVATION_CALLS"
    DOC_BACK_RESERVATION_CALLS="DOC_BACK_RESERVATION_CALLS"
    FACE_ISO_RESERVATION_CALLS="FACE_ISO_RESERVATION_CALLS"
    COMPARE_RESERVATION_CALLS="COMPARE_RESERVATION_CALLS"
class ParameterValidator:
    def __init__(self):
        self.__parameter = {}
        self.__populate_parameters()
        self.__billing_reservation_parameters = [

            PARAMETERS.DOC_FRONT_RESERVATION_CALLS,
            PARAMETERS.DOC_BACK_RESERVATION_CALLS,
            PARAMETERS.COMPARE_RESERVATION_CALLS,
            PARAMETERS.FACE_RESERVATION_CALLS,
            PARAMETERS.ESTIMATE_AGE_RESERVATION_CALLS,
            PARAMETERS.FACE_ISO_RESERVATION_CALLS,
        ]

    def __populate_parameters(self):
        self.__parameter[PARAMETERS.INPUT_IMAGE_FORMAT] = self.Parameter(
            name=PARAMETERS.INPUT_IMAGE_FORMAT, _type="ANY")
        self.__parameter[PARAMETERS.CONTEXT_STRING] = self.Parameter(
            name=PARAMETERS.CONTEXT_STRING, _type="ANY")
        self.__parameter[PARAMETERS.INPUT_TYPE] = self.Parameter(
            name=PARAMETERS.INPUT_TYPE, _type="ANY")
        self.__parameter[PARAMETERS.CONF_SCORE_THR_ENROLL] = self.Parameter(
            name=PARAMETERS.CONF_SCORE_THR_ENROLL, _type="ANY")
        self.__parameter[PARAMETERS.CONF_SCORE_THR_PREDICT] = self.Parameter(
            name=PARAMETERS.CONF_SCORE_THR_PREDICT, _type="ANY")
        self.__parameter[PARAMETERS.BLUR_THRESHOLD_ENROLL_PRED] = self.Parameter(
            name=PARAMETERS.BLUR_THRESHOLD_ENROLL_PRED, _type="ANY")
        self.__parameter[PARAMETERS.THRESHOLD_PROFILE_ENROLL] = self.Parameter(
            name=PARAMETERS.THRESHOLD_PROFILE_ENROLL, _type="ANY")
        self.__parameter[PARAMETERS.THRESHOLD_HIGH_VERTICAL_ENROLL] = self.Parameter(
            name=PARAMETERS.THRESHOLD_HIGH_VERTICAL_ENROLL, _type="ANY")
        self.__parameter[PARAMETERS.THRESHOLD_DOWN_VERTICAL_ENROLL] = self.Parameter(
            name=PARAMETERS.THRESHOLD_DOWN_VERTICAL_ENROLL, _type="ANY")
        self.__parameter[PARAMETERS.THRESHOLD_USER_RIGHT] = self.Parameter(
            name=PARAMETERS.THRESHOLD_USER_RIGHT, _type="ANY")
        self.__parameter[PARAMETERS.THRESHOLD_USER_LEFT] = self.Parameter(
            name=PARAMETERS.THRESHOLD_USER_LEFT, _type="ANY")
        self.__parameter[PARAMETERS.THRESHOLD_USER_TOO_FAR] = self.Parameter(
            name=PARAMETERS.THRESHOLD_USER_TOO_FAR, _type="ANY")
        self.__parameter[PARAMETERS.THRESHOLD_USER_TOO_CLOSE] = self.Parameter(
            name=PARAMETERS.THRESHOLD_USER_TOO_CLOSE, _type="ANY")
        self.__parameter[PARAMETERS.ANGLE_ROTATION_LEFT_THRESHOLD] = self.Parameter(
            name=PARAMETERS.ANGLE_ROTATION_LEFT_THRESHOLD, _type="ANY")
        self.__parameter[PARAMETERS.ANGLE_ROTATION_RIGHT_THRESHOLD] = self.Parameter(
            name=PARAMETERS.ANGLE_ROTATION_RIGHT_THRESHOLD, _type="ANY")
        self.__parameter[PARAMETERS.FACE_TOO_BRIGHT] = self.Parameter(
            name=PARAMETERS.FACE_TOO_BRIGHT, _type="ANY")
        self.__parameter[PARAMETERS.FACE_TOO_DARK] = self.Parameter(
            name=PARAMETERS.FACE_TOO_DARK, _type="ANY")
        self.__parameter[PARAMETERS.DOC_FRONT_RESERVATION_CALLS] = self.Parameter(
            name=PARAMETERS.DOC_FRONT_RESERVATION_CALLS, _type="ANY")
        self.__parameter[PARAMETERS.DOC_FRONT_RESERVATION_CALLS] = self.Parameter(
            name=PARAMETERS.DOC_FRONT_RESERVATION_CALLS, _type="ANY")
        self.__parameter[PARAMETERS.DOC_BACK_RESERVATION_CALLS] = self.Parameter(
            name=PARAMETERS.DOC_BACK_RESERVATION_CALLS, _type="ANY")
        self.__parameter[PARAMETERS.COMPARE_RESERVATION_CALLS] = self.Parameter(
            name=PARAMETERS.COMPARE_RESERVATION_CALLS, _type="ANY")
        self.__parameter[PARAMETERS.FACE_RESERVATION_CALLS] = self.Parameter(
            name=PARAMETERS.FACE_RESERVATION_CALLS, _type="ANY")
        self.__parameter[PARAMETERS.ESTIMATE_AGE_RESERVATION_CALLS] = self.Parameter(
            name=PARAMETERS.ESTIMATE_AGE_RESERVATION_CALLS, _type="ANY")
        self.__parameter[PARAMETERS.FACE_ISO_RESERVATION_CALLS] = self.Parameter(
            name=PARAMETERS.FACE_ISO_RESERVATION_CALLS, _type="ANY")
        self.__parameter[PARAMETERS.SKIP_ANTISPOOF] = self.Parameter(
            name=PARAMETERS.SKIP_ANTISPOOF, _type="ANY")
        self.__parameter[PARAMETERS.SPOOF_FILTER_THRESHOLD] = self.Parameter(
            name=PARAMETERS.SPOOF_FILTER_THRESHOLD, _type="ANY")
        self.__parameter[PARAMETERS.SINGLE_FACE_AGE_RESUL] = self.Parameter(
            name=PARAMETERS.SINGLE_FACE_AGE_RESUL, _type="ANY")


    def validate(self, key, value):
        return self.__parameter[key].validate(value)

    def is_billing_parameter(self, key):
        return key in self.__billing_reservation_parameters

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
            if not self._validate_parameter.is_billing_parameter(key):
                config_param_dict[key.value] = value

        if len(config_param_dict) == 0:
            return None
        return json.dumps(config_param_dict)

    def get_config_billing_param(self):
        if len(self._config_param) == 0:
            return None
        config_billing_param = {}
        for key, value in self._config_param.items():
            if self._validate_parameter.is_billing_parameter(key):
                config_billing_param[key.value] = value

        if len(config_billing_param) == 0:
            return None
        return json.dumps(config_billing_param)

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

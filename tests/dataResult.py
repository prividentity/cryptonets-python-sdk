import pathlib
import sys

src_path = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(src_path))

from src.cryptonets_python_sdk.helper.result_objects.compareResult import (
    FaceCompareResult,
)
from src.cryptonets_python_sdk.helper.result_objects.deleteResult import (
    FaceDeleteResult,
)
from src.cryptonets_python_sdk.helper.result_objects.enrollPredictResult import (
    FaceEnrollPredictResult,
)
from src.cryptonets_python_sdk.helper.result_objects.faceValidationResult import (
    FaceValidationResult,
)
from src.cryptonets_python_sdk.helper.result_objects.isoFaceResult import ISOFaceResult
from src.cryptonets_python_sdk.helper.messages import Message
from src.cryptonets_python_sdk.helper.utils import FaceValidationCode


class Jpg1:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=0,
            message="OK",
            iso_image_height=480,
            iso_image_width=360,
            iso_image_channels=3,
            confidence=0.8549543619155884,
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.ValidBiometric.value,
            second_validation_result=FaceValidationCode.ValidBiometric.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS, message="OK"
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            message="OK",
            enroll_level=1,
        )
        self.delete_result = FaceDeleteResult(status=0, message="OK")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=0,
            message="ValidBiometric",
            top_left_coordinate={"x": 92.5, "y": 147.0},
            bottom_right_coordinate={"x": 287.5, "y": 325.0},
        )
        self.estimate_age_result.append_face_objects(
            return_code=0,
            message="ValidBiometric",
            age=30.03302001953125,
            top_left_coordinate={"x": 92.5, "y": 147.0},
            bottom_right_coordinate={"x": 287.5, "y": 325.0},
        )


class Jpg2:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=0,
            message="OK",
            iso_image_height=480,
            iso_image_width=360,
            iso_image_channels=3,
            confidence=0.8549543619155884,
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.GlassesOn.value,
            second_validation_result=FaceValidationCode.GlassesOn.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-100,
            message="Invalid Image",
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-1,
            message="User not enrolled",
        )
        self.delete_result = FaceDeleteResult(status=-1, message="Missing PUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=10,
            message="GlassesOn",
            top_left_coordinate={"x": 36.0, "y": 74.0},
            bottom_right_coordinate={"x": 138.0, "y": 178.0},
        )
        self.estimate_age_result.append_face_objects(
            return_code=10,
            message="GlassesOn",
            age=41.77806091308594,
            top_left_coordinate={"x": 36.0, "y": 74.0},
            bottom_right_coordinate={"x": 138.0, "y": 178.0},
        )


class Png5:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=12, message="ISO face validation failed."
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.ChinTooFarLeft.value,
            second_validation_result=FaceValidationCode.ChinTooFarLeft.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-100,
            message="Invalid Image",
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-1,
            message="User not enrolled",
        )
        self.delete_result = FaceDeleteResult(message="Missing PUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=12,
            message="ChinTooFarLeft",
            top_left_coordinate={"x": 206.0, "y": 111.0},
            bottom_right_coordinate={"x": 352.0, "y": 259.0},
        )
        self.estimate_age_result.append_face_objects(
            return_code=12,
            message="ChinTooFarLeft",
            age=-1.0,
            top_left_coordinate={"x": 206.0, "y": 111.0},
            bottom_right_coordinate={"x": 352.0, "y": 259.0},
        )


class Png8:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=0,
            message="OK",
            iso_image_height=480,
            iso_image_width=360,
            iso_image_channels=3,
            confidence=0.7746248245239258,
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=0,
            second_validation_result=0,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS, message="OK"
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            message="OK",
            enroll_level=1,
        )
        self.delete_result = FaceDeleteResult(status=0, message="OK")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=0,
            message="ValidBiometric",
            top_left_coordinate={"x": 78.5, "y": 144.0},
            bottom_right_coordinate={"x": 259.5, "y": 314.0},
        )
        self.estimate_age_result.append_face_objects(
            return_code=0,
            message="ValidBiometric",
            age=51.14837646484375,
            top_left_coordinate={"x": 78.5, "y": 144.0},
            bottom_right_coordinate={"x": 259.5, "y": 314.0},
        )


class Png15:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=13, message="ISO face validation failed."
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.ChinTooFarRight.value,
            second_validation_result=FaceValidationCode.ChinTooFarRight.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-100,
            message="Invalid Image",
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-1,
            message="User not enrolled",
        )
        self.delete_result = FaceDeleteResult(message="Missing PUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=13,
            message="ChinTooFarRight",
            top_left_coordinate={"x": 774.0, "y": 374.5},
            bottom_right_coordinate={"x": 1302.0, "y": 935.5},
        )
        self.estimate_age_result.append_face_objects(
            return_code=13,
            message="ChinTooFarRight",
            age=-1.0,
            top_left_coordinate={"x": 774.0, "y": 374.5},
            bottom_right_coordinate={"x": 1302.0, "y": 935.5},
        )


class Png16:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=13, message="ISO face validation failed."
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.ValidBiometric.value,
            second_validation_result=FaceValidationCode.ValidBiometric.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-100,
            message="Invalid Image",
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-1,
            message="User not enrolled",
        )
        self.delete_result = FaceDeleteResult(message="Missing PUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 342.0, "y": 122.0},
            bottom_right_coordinate={"x": 490.0, "y": 270.0},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.NoFace.value,
            message=FaceValidationCode.NoFace.name,
            top_left_coordinate={"x": 45.0, "y": 110.0},
            bottom_right_coordinate={"x": 187.0, "y": 242.0},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 637.5, "y": 128.5},
            bottom_right_coordinate={"x": 776.5, "y": 265.5},
        )

        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ChinTooFarRight.value,
            message=FaceValidationCode.ChinTooFarRight.name,
            age=-1,
            top_left_coordinate={"x": 342.0, "y": 122.0},
            bottom_right_coordinate={"x": 490.0, "y": 270.0},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.NoFace.value,
            message=FaceValidationCode.NoFace.name,
            age=-1.0,
            top_left_coordinate={"x": 45.0, "y": 110.0},
            bottom_right_coordinate={"x": 187.0, "y": 242.0},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=22.1702880859375,
            top_left_coordinate={"x": 637.5, "y": 128.5},
            bottom_right_coordinate={"x": 776.5, "y": 265.5},
        )


class Png17:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=12, message="ISO face validation failed."
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.ValidBiometric.value,
            second_validation_result=FaceValidationCode.ValidBiometric.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-100,
            message="Invalid Image",
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-1,
            message="User not enrolled",
        )
        self.delete_result = FaceDeleteResult(message="Missing PUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 431.0, "y": 123.0},
            bottom_right_coordinate={"x": 575.0, "y": 271.0},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 83.0, "y": 124.5},
            bottom_right_coordinate={"x": 227.0, "y": 265.5},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 724.0, "y": 104.0},
            bottom_right_coordinate={"x": 852.0, "y": 240.0},
        )

        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ChinTooFarLeft.value,
            message=FaceValidationCode.ChinTooFarLeft.name,
            age=-1,
            top_left_coordinate={"x": 431.0, "y": 123.0},
            bottom_right_coordinate={"x": 575.0, "y": 271.0},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=21.73577117919922,
            top_left_coordinate={"x": 83.0, "y": 124.5},
            bottom_right_coordinate={"x": 227.0, "y": 265.5},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ChinTooFarLeft.value,
            message=FaceValidationCode.ChinTooFarLeft.name,
            age=-1,
            top_left_coordinate={"x": 724.0, "y": 104.0},
            bottom_right_coordinate={"x": 852.0, "y": 240.0},
        )


class Jpg18:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=0,
            message="OK",
            iso_image_height=480,
            iso_image_width=360,
            iso_image_channels=3,
            confidence=0.9994304776191711,
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=0,
            second_validation_result=0,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS, message="OK"
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            message="OK",
            enroll_level=1,
        )
        self.delete_result = FaceDeleteResult(status=0, message="OK")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=0,
            message="ValidBiometric",
            top_left_coordinate={"x": 187.0, "y": 153.0},
            bottom_right_coordinate={"x": 381.0, "y": 333.0},
        )
        self.estimate_age_result.append_face_objects(
            return_code=0,
            message="ValidBiometric",
            age=38.61371994018555,
            top_left_coordinate={"x": 187.0, "y": 153.0},
            bottom_right_coordinate={"x": 381.0, "y": 333.0},
        )


class Jpg19:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=3, message="ISO face validation failed."
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.ValidBiometric.value,
            second_validation_result=FaceValidationCode.ValidBiometric.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS, message="OK"
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            message="OK",
            enroll_level=1,
        )
        self.delete_result = FaceDeleteResult(status=0, message="OK")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 109.0, "y": 71.5},
            bottom_right_coordinate={"x": 143.0, "y": 106.5},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 288.0, "y": 66.5},
            bottom_right_coordinate={"x": 314.0, "y": 93.5},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=25.013702392578125,
            top_left_coordinate={"x": 109.0, "y": 71.5},
            bottom_right_coordinate={"x": 143.0, "y": 106.5},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=25.790895462036133,
            top_left_coordinate={"x": 288.0, "y": 66.5},
            bottom_right_coordinate={"x": 314.0, "y": 93.5},
        )


class Jpg20:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=0,
            message="OK",
            iso_image_height=480,
            iso_image_width=360,
            iso_image_channels=3,
            confidence=0.9994304776191711,
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.ValidBiometric.value,
            second_validation_result=FaceValidationCode.ValidBiometric.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS, message="OK"
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            message="OK",
            enroll_level=1,
        )
        self.delete_result = FaceDeleteResult(status=0, message="OK")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 59.0, "y": 48.5},
            bottom_right_coordinate={"x": 99.0, "y": 89.5},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 279.0, "y": 56.5},
            bottom_right_coordinate={"x": 319.0, "y": 99.5},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 168.5, "y": 67.0},
            bottom_right_coordinate={"x": 205.5, "y": 107.0},
        )

        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=14.596866607666016,
            top_left_coordinate={"x": 59.0, "y": 48.5},
            bottom_right_coordinate={"x": 99.0, "y": 89.5},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=17.12334632873535,
            top_left_coordinate={"x": 279.0, "y": 56.5},
            bottom_right_coordinate={"x": 319.0, "y": 99.5},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=11.554624557495117,
            top_left_coordinate={"x": 168.5, "y": 67.0},
            bottom_right_coordinate={"x": 205.5, "y": 107.0},
        )


class Jpg3:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=FaceValidationCode.FaceTooDark.value,
            message="ISO face validation failed.",
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.FaceTooDark.value,
            second_validation_result=FaceValidationCode.FaceTooDark.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS, message="Ok"
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            message="Ok",
            enroll_level=1,
        )
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.FaceTooDark.value,
            message=FaceValidationCode.FaceTooDark.name,
            top_left_coordinate={"x": 89.0, "y": 93.5},
            bottom_right_coordinate={"x": 187.0, "y": 186.5},
        )

        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.FaceTooDark.value,
            message=FaceValidationCode.FaceTooDark.name,
            age=-1,
            top_left_coordinate={"x": 89.0, "y": 93.5},
            bottom_right_coordinate={"x": 187.0, "y": 186.5},
        )


class Jpeg4:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=0,
            message="OK",
            iso_image_height=480,
            iso_image_width=360,
            iso_image_channels=3,
            confidence=0.9904078841209412,
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.ValidBiometric.value,
            second_validation_result=FaceValidationCode.ValidBiometric.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS, message="Ok"
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            message="Ok",
            enroll_level=1,
        )
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 100.5, "y": 63.0},
            bottom_right_coordinate={"x": 193.5, "y": 159.0},
        )

        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=23.95326805114746,
            top_left_coordinate={"x": 100.5, "y": 63.0},
            bottom_right_coordinate={"x": 193.5, "y": 159.0},
        )


class Jpeg9:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=0,
            message="OK",
            iso_image_height=480,
            iso_image_width=360,
            iso_image_channels=3,
            confidence=0.9994041919708252,
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.ValidBiometric.value,
            second_validation_result=FaceValidationCode.ValidBiometric.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS, message="Ok"
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-1,
            message="User not enrolled",
            enroll_level=None,
        )
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 279.0, "y": 106.5},
            bottom_right_coordinate={"x": 381.0, "y": 215.5},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 495.5, "y": 105.0},
            bottom_right_coordinate={"x": 596.5, "y": 213.0},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 56.5, "y": 117.5},
            bottom_right_coordinate={"x": 157.5, "y": 224.5},
        )

        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=53.590492248535156,
            top_left_coordinate={"x": 279.0, "y": 106.5},
            bottom_right_coordinate={"x": 381.0, "y": 215.5},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=54.85247039794922,
            top_left_coordinate={"x": 495.5, "y": 105.0},
            bottom_right_coordinate={"x": 596.5, "y": 213.0},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=53.274375915527344,
            top_left_coordinate={"x": 56.5, "y": 117.5},
            bottom_right_coordinate={"x": 157.5, "y": 224.5},
        )


class Jpeg10:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=-100, message="ISO face validation failed."
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=0,
            second_validation_result=0,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-100,
            message="Invalid Image",
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-1,
            message="User not enrolled",
        )
        self.delete_result = FaceDeleteResult(status=-1, message="Missing PUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=0,
            message="ValidBiometric",
            top_left_coordinate={"x": 114.5, "y": 49.0},
            bottom_right_coordinate={"x": 151.5, "y": 85.0},
        )

        self.estimate_age_result.append_face_objects(
            return_code=0,
            message="ValidBiometric",
            age=28.262521743774414,
            top_left_coordinate={"x": 114.5, "y": 49.0},
            bottom_right_coordinate={"x": 151.5, "y": 85.0},
        )


class Jpeg12:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=0,
            message="OK",
            iso_image_height=480,
            iso_image_width=360,
            iso_image_channels=3,
            confidence=0.9678338766098022,
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.ValidBiometric.value,
            second_validation_result=FaceValidationCode.ValidBiometric.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS, message="Ok"
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            message="Ok",
            enroll_level=1,
        )
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 151.5, "y": 478.5},
            bottom_right_coordinate={"x": 548.5, "y": 913.5},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 881.0, "y": 330.5},
            bottom_right_coordinate={"x": 1281.0, "y": 757.5},
        )

        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=18.01043701171875,
            top_left_coordinate={"x": 151.5, "y": 478.5},
            bottom_right_coordinate={"x": 548.5, "y": 913.5},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=19.81570816040039,
            top_left_coordinate={"x": 881.0, "y": 330.5},
            bottom_right_coordinate={"x": 1281.0, "y": 757.5},
        )


class Jpeg13:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=FaceValidationCode.ChinTooFarRight.value,
            message="ISO face validation failed.",
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.ChinTooFarRight.value,
            second_validation_result=FaceValidationCode.ChinTooFarRight.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-100,
            message="Invalid Image",
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-1,
            message="User not enrolled",
        )
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.NoFace.value,
            message=FaceValidationCode.NoFace.name,
            top_left_coordinate={"x": 396.5, "y": 74.5},
            bottom_right_coordinate={"x": 507.5, "y": 183.5},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ChinTooFarRight.value,
            message=FaceValidationCode.ChinTooFarRight.name,
            top_left_coordinate={"x": 207.0, "y": 81.0},
            bottom_right_coordinate={"x": 313.0, "y": 189.0},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 35.0, "y": 86.0},
            bottom_right_coordinate={"x": 131.0, "y": 184.0},
        )

        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ChinTooFarRight.value,
            message=FaceValidationCode.ChinTooFarRight.name,
            age=-1,
            top_left_coordinate={"x": 396.5, "y": 74.5},
            bottom_right_coordinate={"x": 507.5, "y": 183.5},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ChinTooFarRight.value,
            message=FaceValidationCode.ChinTooFarRight.name,
            age=-1,
            top_left_coordinate={"x": 207.0, "y": 81.0},
            bottom_right_coordinate={"x": 313.0, "y": 189.0},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=22.285966873168945,
            top_left_coordinate={"x": 35.0, "y": 86.0},
            bottom_right_coordinate={"x": 131.0, "y": 184.0},
        )


class Png6:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=-100, message="ISO face validation failed."
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=-1,
            first_validation_result=FaceValidationCode.InvalidImage.value,
            second_validation_result=FaceValidationCode.InvalidImage.value,
            message="",
        )
        # The returned message for this file for both predict and enroll tests should be something like 'invalid image'
        # but there are 2 problems here:
        # -1- in messages.py there is no such defined as 'invalid image'
        # -2- In the cpp code base, the operation enrol & predict does not return a message at all in this case
        # (invalid face)
        # -3- There is no such message generic 'something went wrong while doing predict' returned by c++ code
        #  anywhere in the c++.
        # As The specification is unclear about let's put with the generic 'EXCEPTION_ERROR_ENROLL' and 'EXCEPTION_ERROR_PREDICT'
        # that is assigned by the python testing (se FaceModule) code **which is wrong as we want to test the real
        # message returned by the API not a made up message by the testing code!**
        # TODO FIX ME
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-100,
            message=Message().EXCEPTION_ERROR_ENROLL,
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-100,
            message=Message().EXCEPTION_ERROR_PREDICT,
        )
        self.delete_result = FaceDeleteResult(message="Missing PUID")
        self.set_face_objects()

    def set_face_objects(self):
        pass


class Png7:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=-100, message="ISO face validation failed."
        )
        self.compare_result = FaceCompareResult(
            status=0,
            message="",
            result=-1,
            first_validation_result=FaceValidationCode.InvalidImage.value,
            second_validation_result=FaceValidationCode.InvalidImage.value,
        )
        # TODO FIX ME  same as 6.png comment
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-100,
            message=Message().EXCEPTION_ERROR_ENROLL,
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            code=-100,
            message=Message().EXCEPTION_ERROR_PREDICT,
        )
        self.delete_result = FaceDeleteResult(message="Missing PUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=-1,
            message="NoFace",
            top_left_coordinate={"x": 236.5, "y": 143.5},
            bottom_right_coordinate={"x": 357.5, "y": 246.5},
        )

        self.estimate_age_result.append_face_objects(
            return_code=-1,
            message="NoFace",
            age=-1,
            top_left_coordinate={"x": 236.5, "y": 143.5},
            bottom_right_coordinate={"x": 357.5, "y": 246.5},
        )


class Png11:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=19, message="ISO face validation failed."
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=FaceValidationCode.ValidBiometric.value,
            second_validation_result=FaceValidationCode.ValidBiometric.value,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS, message="Ok"
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            message="Ok",
            enroll_level=1,
        )
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 233.5, "y": 178.0},
            bottom_right_coordinate={"x": 368.5, "y": 312.0},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            top_left_coordinate={"x": 429.5, "y": 123.5},
            bottom_right_coordinate={"x": 548.5, "y": 246.5},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.NoFace.value,
            message=FaceValidationCode.NoFace.name,
            top_left_coordinate={"x": 65.5, "y": 108.5},
            bottom_right_coordinate={"x": 180.5, "y": 223.5},
        )
        self.is_valid_result.append_face_objects(
            return_code=FaceValidationCode.NoFace.value,
            message=FaceValidationCode.NoFace.name,
            top_left_coordinate={"x": 36.5, "y": 349.0},
            bottom_right_coordinate={"x": 89.5, "y": 401.0},
        )

        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=24.499250411987305,
            top_left_coordinate={"x": 233.5, "y": 178.0},
            bottom_right_coordinate={"x": 368.5, "y": 312.0},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.ValidBiometric.value,
            message=FaceValidationCode.ValidBiometric.name,
            age=42.65743637084961,
            top_left_coordinate={"x": 429.5, "y": 123.5},
            bottom_right_coordinate={"x": 548.5, "y": 246.5},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.NoFace.value,
            message=FaceValidationCode.NoFace.name,
            age=-1,
            top_left_coordinate={"x": 65.5, "y": 108.5},
            bottom_right_coordinate={"x": 180.5, "y": 223.5},
        )
        self.estimate_age_result.append_face_objects(
            return_code=FaceValidationCode.NoFace.value,
            message=FaceValidationCode.NoFace.name,
            age=-1,
            top_left_coordinate={"x": 36.5, "y": 349.0},
            bottom_right_coordinate={"x": 89.5, "y": 401.0},
        )


class Jpg14:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(
            status=0,
            message="OK",
            iso_image_height=480,
            iso_image_width=360,
            iso_image_channels=3,
            confidence=0.9276024103164673,
        )
        self.compare_result = FaceCompareResult(
            status=FaceCompareResult.CALL_STATUS_SUCCESS,
            result=1,
            first_validation_result=0,
            second_validation_result=0,
        )
        self.enroll_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS, message="Ok"
        )
        self.predict_result = FaceEnrollPredictResult(
            status=FaceEnrollPredictResult.CALL_STATUS_SUCCESS,
            message="Ok",
            enroll_level=1,
        )
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(
            return_code=0,
            message="ValidBiometric",
            top_left_coordinate={"x": 298.0, "y": 465.0},
            bottom_right_coordinate={"x": 554.0, "y": 739.0},
        )
        self.is_valid_result.append_face_objects(
            return_code=0,
            message="ValidBiometric",
            top_left_coordinate={"x": 699.0, "y": 334.0},
            bottom_right_coordinate={"x": 949.0, "y": 590.0},
        )

        self.estimate_age_result.append_face_objects(
            return_code=0,
            message="ValidBiometric",
            age=9.415367126464844,
            top_left_coordinate={"x": 298.0, "y": 465.0},
            bottom_right_coordinate={"x": 554.0, "y": 739.0},
        )
        self.estimate_age_result.append_face_objects(
            return_code=0,
            message="ValidBiometric",
            age=11.386466979980469,
            top_left_coordinate={"x": 699.0, "y": 334.0},
            bottom_right_coordinate={"x": 949.0, "y": 590.0},
        )

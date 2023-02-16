import pathlib
import sys

src_path = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(src_path))

from src.cryptonets_python_sdk.helper.result_objects.compareResult import FaceCompareResult
from src.cryptonets_python_sdk.helper.result_objects.deleteResult import FaceDeleteResult
from src.cryptonets_python_sdk.helper.result_objects.enrollPredictResult import FaceEnrollPredictResult
from src.cryptonets_python_sdk.helper.result_objects.faceValidationResult import FaceValidationResult
from src.cryptonets_python_sdk.helper.result_objects.isoFaceResult import ISOFaceResult


class Jpg1:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=9, message="ISO face validation failed.")
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=0, message="OK")
        self.predict_result = FaceEnrollPredictResult(status=0, message="OK")
        self.delete_result = FaceDeleteResult(status=0, message="OK")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 92.5, "y": 147.0},
                                                 bottom_right_coordinate={"x": 287.5, "y": 325.0})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=30.03302001953125,
                                                     top_left_coordinate={"x": 92.5, "y": 147.0},
                                                     bottom_right_coordinate={"x": 287.5, "y": 325.0})


class Jpg2:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=0, message="OK", iso_image_height=480, iso_image_width=360,
                                            iso_image_channels=3, confidence=0.8549543619155884)
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=-100, message="Invalid Image")
        self.predict_result = FaceEnrollPredictResult(status=-1, message="User not enrolled")
        self.delete_result = FaceDeleteResult(status=-1, message="Missing UUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=10, message="GlassesOn",
                                                 top_left_coordinate={"x": 36.0, "y": 74.0},
                                                 bottom_right_coordinate={"x": 138.0, "y": 178.0})
        self.estimate_age_result.append_face_objects(return_code=10, message="GlassesOn", age=41.77806091308594,
                                                     top_left_coordinate={"x": 36.0, "y": 74.0},
                                                     bottom_right_coordinate={"x": 138.0, "y": 178.0})


class Png5:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=12, message="ISO face validation failed.")
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=-100, message="Invalid Image")
        self.predict_result = FaceEnrollPredictResult(status=-1, message="User not enrolled")
        self.delete_result = FaceDeleteResult(message="Missing UUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=12, message="ChinTooFarLeft",
                                                 top_left_coordinate={"x": 205.0, "y": 110.5},
                                                 bottom_right_coordinate={"x": 351.0, "y": 259.5})
        self.estimate_age_result.append_face_objects(return_code=12, message="ChinTooFarLeft", age=-1.0,
                                                     top_left_coordinate={"x": 205.0, "y": 110.5},
                                                     bottom_right_coordinate={"x": 351.0, "y": 259.5})


class Png8:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=0, message="OK", iso_image_height=480, iso_image_width=360,
                                            iso_image_channels=3, confidence=0.7746248245239258)
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=0, message="OK")
        self.predict_result = FaceEnrollPredictResult(status=0, message="OK")
        self.delete_result = FaceDeleteResult(status=0, message="OK")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 78.5, "y": 144.0},
                                                 bottom_right_coordinate={"x": 259.5, "y": 314.0})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=51.14837646484375,
                                                     top_left_coordinate={"x": 78.5, "y": 144.0},
                                                     bottom_right_coordinate={"x": 259.5, "y": 314.0})


class Png15:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=13, message="ISO face validation failed.")
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=-100, message="Invalid Image")
        self.predict_result = FaceEnrollPredictResult(status=-1, message="User not enrolled")
        self.delete_result = FaceDeleteResult(message="Missing UUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=13, message="ChinTooFarRight",
                                                 top_left_coordinate={"x": 774.5, "y": 374.5},
                                                 bottom_right_coordinate={"x": 1303.5, "y": 935.5})
        self.estimate_age_result.append_face_objects(return_code=13, message="ChinTooFarRight", age=-1.0,
                                                     top_left_coordinate={"x": 774.5, "y": 374.5},
                                                     bottom_right_coordinate={"x": 1303.5, "y": 935.5})


class Png16:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=13, message="ISO face validation failed.")
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=-100, message="Invalid Image")
        self.predict_result = FaceEnrollPredictResult(status=-1, message="User not enrolled")
        self.delete_result = FaceDeleteResult(message="Missing UUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 341.5, "y": 121.0},
                                                 bottom_right_coordinate={"x": 490.5, "y": 269.0})
        self.is_valid_result.append_face_objects(return_code=-1, message="NoFace",
                                                 top_left_coordinate={"x": 42.0, "y": 109.5},
                                                 bottom_right_coordinate={"x": 188.0, "y": 244.5})
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 637.0, "y": 129.0},
                                                 bottom_right_coordinate={"x": 777.0, "y": 265.0})
        self.estimate_age_result.append_face_objects(return_code=13, message="ChinTooFarRight", age=-1,
                                                     top_left_coordinate={"x": 341.5, "y": 121.0},
                                                     bottom_right_coordinate={"x": 490.5, "y": 269.0})
        self.estimate_age_result.append_face_objects(return_code=-1, message="NoFace", age=-1.0,
                                                     top_left_coordinate={"x": 42.0, "y": 109.5},
                                                     bottom_right_coordinate={"x": 188.0, "y": 244.5})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=22.1702880859375,
                                                     top_left_coordinate={"x": 637.0, "y": 129.0},
                                                     bottom_right_coordinate={"x": 777.0, "y": 265.0})


class Png17:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=12, message="ISO face validation failed.")
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=-100, message="Invalid Image")
        self.predict_result = FaceEnrollPredictResult(status=-1, message="User not enrolled")
        self.delete_result = FaceDeleteResult(message="Missing UUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 432.0, "y": 123.0},
                                                 bottom_right_coordinate={"x": 576.0, "y": 271.0})
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 82.5, "y": 125.5},
                                                 bottom_right_coordinate={"x": 227.5, "y": 264.5})
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 722.0, "y": 102.5},
                                                 bottom_right_coordinate={"x": 850.0, "y": 237.5})
        self.estimate_age_result.append_face_objects(return_code=12, message="ChinTooFarLeft", age=-1,
                                                     top_left_coordinate={"x": 432.0, "y": 123.0},
                                                     bottom_right_coordinate={"x": 576.0, "y": 271.0})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=21.73577117919922,
                                                     top_left_coordinate={"x": 82.5, "y": 125.5},
                                                     bottom_right_coordinate={"x": 227.5, "y": 264.5})
        self.estimate_age_result.append_face_objects(return_code=12, message="ChinTooFarLeft", age=-1,
                                                     top_left_coordinate={"x": 722.0, "y": 102.5},
                                                     bottom_right_coordinate={"x": 850.0, "y": 237.5})


class Jpg18:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=0, message="OK", iso_image_height=480, iso_image_width=360,
                                            iso_image_channels=3, confidence=0.9994304776191711)
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=0, message="OK")
        self.predict_result = FaceEnrollPredictResult(status=0, message="OK")
        self.delete_result = FaceDeleteResult(status=0, message="OK")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 187.0, "y": 153.0},
                                                 bottom_right_coordinate={"x": 381.0, "y": 333.0})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=38.61371994018555,
                                                     top_left_coordinate={"x": 187.0, "y": 153.0},
                                                     bottom_right_coordinate={"x": 381.0, "y": 333.0})


class Jpg19:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=0, message="OK", iso_image_height=480, iso_image_width=360,
                                            iso_image_channels=3, confidence=0.11450446397066116)
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=0, message="OK")
        self.predict_result = FaceEnrollPredictResult(status=0, message="OK")
        self.delete_result = FaceDeleteResult(status=0, message="OK")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 107.5, "y": 72.0},
                                                 bottom_right_coordinate={"x": 144.5, "y": 110.0})
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 286.5, "y": 69.0},
                                                 bottom_right_coordinate={"x": 315.5, "y": 97.0})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=25.008012771606445,
                                                     top_left_coordinate={"x": 107.5, "y": 72.0},
                                                     bottom_right_coordinate={"x": 144.5, "y": 110.0})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=24.311437606811523,
                                                     top_left_coordinate={"x": 286.5, "y": 69.0},
                                                     bottom_right_coordinate={"x": 315.5, "y": 97.0})


class Jpg20:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=9, message="ISO face validation failed.")
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=0, message="OK")
        self.predict_result = FaceEnrollPredictResult(status=0, message="OK")
        self.delete_result = FaceDeleteResult(status=0, message="OK")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 58.5, "y": 48.0},
                                                 bottom_right_coordinate={"x": 99.5, "y": 90.0})
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 279.0, "y": 57.5},
                                                 bottom_right_coordinate={"x": 319.0, "y": 100.5})
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 168.5, "y": 67.0},
                                                 bottom_right_coordinate={"x": 205.5, "y": 107.0})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=14.596866607666016,
                                                     top_left_coordinate={"x": 58.5, "y": 48.0},
                                                     bottom_right_coordinate={"x": 99.5, "y": 90.0})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=18.02923011779785,
                                                     top_left_coordinate={"x": 279.0, "y": 57.5},
                                                     bottom_right_coordinate={"x": 319.0, "y": 100.5})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=11.554624557495117,
                                                     top_left_coordinate={"x": 168.5, "y": 67.0},
                                                     bottom_right_coordinate={"x": 205.5, "y": 107.0})


class Jpg3:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=9, message="ISO face validation failed.")
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=0, message="Ok")
        self.predict_result = FaceEnrollPredictResult(status=0, message="Ok")
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 89.0, "y": 93.5},
                                                 bottom_right_coordinate={"x": 187.0, "y": 186.5})

        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=61.46807861328125,
                                                     top_left_coordinate={"x": 89.0, "y": 93.5},
                                                     bottom_right_coordinate={"x": 187.0, "y": 186.5})


class Jpeg4:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=0, message="OK", iso_image_height=480, iso_image_width=360,
                                            iso_image_channels=3, confidence=0.9904078841209412)
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=0, message="Ok")
        self.predict_result = FaceEnrollPredictResult(status=0, message="Ok")
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 100.0, "y": 63.0},
                                                 bottom_right_coordinate={"x": 194.0, "y": 159.0})

        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=24.6011905670166,
                                                     top_left_coordinate={"x": 100.0, "y": 63.0},
                                                     bottom_right_coordinate={"x": 194.0, "y": 159.0})


class Jpeg9:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=0, message="OK", iso_image_height=480, iso_image_width=360,
                                            iso_image_channels=3, confidence=0.9994041919708252)
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=0, message="Ok")
        self.predict_result = FaceEnrollPredictResult(status=0, message="Ok")
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=-1, message="NoFace",
                                                 top_left_coordinate={"x": 279.0, "y": 106.0},
                                                 bottom_right_coordinate={"x": 381.0, "y": 216.0})
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 495.0, "y": 105.0},
                                                 bottom_right_coordinate={"x": 597.0, "y": 213.0})
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 56.5, "y": 117.5},
                                                 bottom_right_coordinate={"x": 157.5, "y": 224.5})

        self.estimate_age_result.append_face_objects(return_code=-1, message="NoFace", age=-1,
                                                     top_left_coordinate={"x": 279.0, "y": 106.0},
                                                     bottom_right_coordinate={"x": 381.0, "y": 216.0})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=54.85247039794922,
                                                     top_left_coordinate={"x": 495.0, "y": 105.0},
                                                     bottom_right_coordinate={"x": 597.0, "y": 213.0})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=53.27436828613281,
                                                     top_left_coordinate={"x": 56.5, "y": 117.5},
                                                     bottom_right_coordinate={"x": 157.5, "y": 224.5})


class Jpeg10:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=-100, message="ISO face validation failed.")
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=-100, message="Invalid Image")
        self.predict_result = FaceEnrollPredictResult(status=-1, message="User not enrolled")
        self.delete_result = FaceDeleteResult(status=-1, message="Missing UUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 114.5, "y": 49.0},
                                                 bottom_right_coordinate={"x": 151.5, "y": 85.0})

        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=28.262521743774414,
                                                     top_left_coordinate={"x": 114.5, "y": 49.0},
                                                     bottom_right_coordinate={"x": 151.5, "y": 85.0})


class Jpeg12:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=0, message="OK", iso_image_height=480, iso_image_width=360,
                                            iso_image_channels=3, confidence=0.9678338766098022)
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=0, message="Ok")
        self.predict_result = FaceEnrollPredictResult(status=0, message="Ok")
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 151.5, "y": 479.0},
                                                 bottom_right_coordinate={"x": 548.5, "y": 913.0})
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 881.0, "y": 330.5},
                                                 bottom_right_coordinate={"x": 1281.0, "y": 757.5})

        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=17.451465606689453,
                                                     top_left_coordinate={"x": 151.5, "y": 479.0},
                                                     bottom_right_coordinate={"x": 548.5, "y": 913.0})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=19.81570816040039,
                                                     top_left_coordinate={"x": 881.0, "y": 330.5},
                                                     bottom_right_coordinate={"x": 1281.0, "y": 757.5})


class Jpeg13:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=13, message="ISO face validation failed.")
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=-100, message="Invalid Image")
        self.predict_result = FaceEnrollPredictResult(status=-1, message="User not enrolled")
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=-1, message="NoFace",
                                                 top_left_coordinate={"x": 393.5, "y": 74.0},
                                                 bottom_right_coordinate={"x": 508.5, "y": 186.0})
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 207.0, "y": 79.0},
                                                 bottom_right_coordinate={"x": 315.0, "y": 189.0})
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 35.5, "y": 86.5},
                                                 bottom_right_coordinate={"x": 130.5, "y": 183.5})

        self.estimate_age_result.append_face_objects(return_code=13, message="ChinTooFarRight", age=-1,
                                                     top_left_coordinate={"x": 393.5, "y": 74.0},
                                                     bottom_right_coordinate={"x": 508.5, "y": 186.0})
        self.estimate_age_result.append_face_objects(return_code=13, message="ChinTooFarRight", age=-1,
                                                     top_left_coordinate={"x": 207.0, "y": 79.0},
                                                     bottom_right_coordinate={"x": 315.0, "y": 189.0})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=22.285968780517578,
                                                     top_left_coordinate={"x": 35.5, "y": 86.5},
                                                     bottom_right_coordinate={"x": 130.5, "y": 183.5})


class Png6:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=-100, message="ISO face validation failed.")
        self.compare_result = FaceCompareResult(status=-1, message="Something went wrong while doing compare.")
        self.enroll_result = FaceEnrollPredictResult(status=-100, message="Invalid Image")
        self.predict_result = FaceEnrollPredictResult(status=-100, message="Invalid Image")
        self.delete_result = FaceDeleteResult(message="Missing UUID")
        self.set_face_objects()

    def set_face_objects(self):
        pass


class Png7:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=-100, message="ISO face validation failed.")
        self.compare_result = FaceCompareResult(status=1, message="",result=1,first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=-100, message="Invalid Image")
        self.predict_result = FaceEnrollPredictResult(status=-100, message="Invalid Image")
        self.delete_result = FaceDeleteResult(message="Missing UUID")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=-1, message="NoFace",
                                                 top_left_coordinate={"x": 236.5, "y": 143.5},
                                                 bottom_right_coordinate={"x": 357.5, "y": 246.5})

        self.estimate_age_result.append_face_objects(return_code=-1, message="NoFace", age=-1,
                                                     top_left_coordinate={"x": 236.5, "y": 143.5},
                                                     bottom_right_coordinate={"x": 357.5, "y": 246.5})


class Png11:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=0, message="OK", iso_image_height=480, iso_image_width=360,
                                            iso_image_channels=3, confidence=0.9949344992637634)
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=0, message="Ok")
        self.predict_result = FaceEnrollPredictResult(status=0, message="Ok")
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 233.5, "y": 178.5},
                                                 bottom_right_coordinate={"x": 368.5, "y": 311.5})
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 429.0, "y": 123.0},
                                                 bottom_right_coordinate={"x": 549.0, "y": 247.0})
        self.is_valid_result.append_face_objects(return_code=-1, message="NoFace",
                                                 top_left_coordinate={"x": 65.5, "y": 108.5},
                                                 bottom_right_coordinate={"x": 180.5, "y": 223.5})
        self.is_valid_result.append_face_objects(return_code=4, message="TooFaraway",
                                                 top_left_coordinate={"x": 34.0, "y": 349.5},
                                                 bottom_right_coordinate={"x": 88.0, "y": 400.5})

        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=24.499250411987305,
                                                     top_left_coordinate={"x": 233.5, "y": 178.5},
                                                     bottom_right_coordinate={"x": 368.5, "y": 311.5})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=43.474491119384766,
                                                     top_left_coordinate={"x": 429.0, "y": 123.0},
                                                     bottom_right_coordinate={"x": 549.0, "y": 247.0})
        self.estimate_age_result.append_face_objects(return_code=-1, message="NoFace", age=-1,
                                                     top_left_coordinate={"x": 65.5, "y": 108.5},
                                                     bottom_right_coordinate={"x": 180.5, "y": 223.5})
        self.estimate_age_result.append_face_objects(return_code=4, message="TooFaraway", age=-1,
                                                     top_left_coordinate={"x": 34.0, "y": 349.5},
                                                     bottom_right_coordinate={"x": 88.0, "y": 400.5})


class Jpg14:
    def __init__(self):
        self.is_valid_result = FaceValidationResult(error=0, message="OK")
        self.estimate_age_result = FaceValidationResult(error=0, message="OK")
        self.get_iso_result = ISOFaceResult(status=0, message="OK", iso_image_height=480, iso_image_width=360,
                                            iso_image_channels=3, confidence=0.9276024103164673)
        self.compare_result = FaceCompareResult(status=1, result=1, first_validation_result=0,
                                                second_validation_result=0)
        self.enroll_result = FaceEnrollPredictResult(status=0, message="Ok")
        self.predict_result = FaceEnrollPredictResult(status=0, message="Ok")
        self.delete_result = FaceDeleteResult(status=0, message="Ok")
        self.set_face_objects()

    def set_face_objects(self):
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 299.0, "y": 465.0},
                                                 bottom_right_coordinate={"x": 555.0, "y": 739.0})
        self.is_valid_result.append_face_objects(return_code=0, message="ValidBiometric",
                                                 top_left_coordinate={"x": 698.0, "y": 334.0},
                                                 bottom_right_coordinate={"x": 948.0, "y": 590.0})

        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=9.415367126464844,
                                                     top_left_coordinate={"x": 299.0, "y": 465.0},
                                                     bottom_right_coordinate={"x": 555.0, "y": 739.0})
        self.estimate_age_result.append_face_objects(return_code=0, message="ValidBiometric", age=11.386466979980469,
                                                     top_left_coordinate={"x": 698.0, "y": 334.0},
                                                     bottom_right_coordinate={"x": 948.0, "y": 590.0})

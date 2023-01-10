import pathlib
import sys
from glob import glob
from timeit import default_timer

from PIL import Image
from termcolor import colored

src_path = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(src_path))
import numpy as np
from cryptonets_python_sdk.settings.configuration import ConfigObject
from cryptonets_python_sdk.settings.configuration import PARAMETERS
from cryptonets_python_sdk.factor import FaceFactor
from cryptonets_python_sdk.settings.loggingLevel import LoggingLevel


def image_path_to_array(image_path: str) -> np.ndarray:
    image = Image.open(image_path).convert('RGB')
    return np.array(image)


def test_compare(compare_face_factor, compare_path, config=None):
    print(colored("{}\n{}".format("Compare", "=" * 25), "green"))
    compare_start_time = default_timer()
    compare_handle = compare_face_factor.compare(image_path_1=compare_path, image_path_2=compare_path, config=config)
    print("Duration:", default_timer() - compare_start_time, "\n")
    print("Status:{}\nResult:{}\nMessage:{}\nMin:{}\nMean:{}\nMax:{}\n1VR:{}\n2VR:{}\n".format(
        compare_handle.status,
        compare_handle.result, compare_handle.message, compare_handle.distance_min,
        compare_handle.distance_mean,
        compare_handle.distance_max, compare_handle.first_validation_result,
        compare_handle.second_validation_result))


def test_predict(predict_face_factor, predict_img_path, config=None):
    print(colored("{}\n{}".format("Predict", "=" * 25), "green"))
    predict_start_time = default_timer()
    predict_handle = predict_face_factor.predict(image_path=predict_img_path, config=config)
    print("Duration:", default_timer() - predict_start_time, "\n")
    print("Status:{}\nMessage:{}\nEnroll Level:{}\nUUID:{}\nGUID:{}\nToken:{}\n".format(predict_handle.status,
                                                                                        predict_handle.message,
                                                                                        predict_handle.enroll_level,
                                                                                        predict_handle.uuid,
                                                                                        predict_handle.guid,
                                                                                        predict_handle.token))
    return predict_handle


def test_enroll(enroll_face_factor, enroll_img_path, config=None):
    print(colored("{}\n{}".format("Enroll", "=" * 25), "green"))
    enroll_start_time = default_timer()
    enroll_handle = enroll_face_factor.enroll(image_path=enroll_img_path, config=config)
    print("Duration:", default_timer() - enroll_start_time, "\n")
    print("Status:{}\nMessage:{}\nEnroll Level:{}\nUUID:{}\nGUID:{}\nToken:{}\n".format(enroll_handle.status,
                                                                                        enroll_handle.message,
                                                                                        enroll_handle.enroll_level,
                                                                                        enroll_handle.uuid,
                                                                                        enroll_handle.guid,
                                                                                        enroll_handle.token))


def test_delete(delete_face_factor, predict_handle):
    print(colored("{}\n{}".format("Delete", "=" * 25), "green"))
    delete_start_time = default_timer()
    delete_handle = delete_face_factor.delete(predict_handle.uuid)
    print("Duration:", default_timer() - delete_start_time, "\n")
    print("Status:{}\nMessage:{}".format(delete_handle.status, delete_handle.message))


def test_age_estimate(age_face_factor, age_path, config=None):
    print(colored("{}\n{}".format("Age Estimation", "=" * 25), "green"))
    age_start_time = default_timer()
    age_handle = age_face_factor.estimate_age(image_path=age_path, config=config)
    print("Duration:", default_timer() - age_start_time, "\n")
    print("Error:{}\nMessage:{}".format(age_handle.error, age_handle.message))
    for index, face in enumerate(age_handle.face_objects):
        print(
            "Face#:{}\n{}\nReturn Code:{}\nMessage:{}\nAge:{}\nBBox TL:{}\nBBox BR:{}\n".format(index + 1, '-' * 7,
                                                                                                face.return_code,
                                                                                                face.message,
                                                                                                face.age,
                                                                                                face.bounding_box.top_left_coordinate.__str__(),
                                                                                                face.bounding_box.bottom_right_coordinate.__str__()))

    if len(age_handle.face_objects) == 0:
        print("No Faces found!!\n")


def test_valid(valid_face_factor, valid_path, config=None):
    print(colored("{}\n{}".format("Is Valid", "=" * 25), "green"))
    valid_start_time = default_timer()
    is_valid_handle = valid_face_factor.is_valid(image_path=valid_path, config=config)
    print("Duration:", default_timer() - valid_start_time, "\n")

    print("Error:{}\nMessage:{}".format(is_valid_handle.error, is_valid_handle.message))
    for index, face in enumerate(is_valid_handle.face_objects):
        print(
            "Face#:{}\n{}\nReturn Code:{}\nMessage:{}\nAge:{}\nBBox TL:{}\nBBox BR:{}\n".format(index + 1, '-' * 7,
                                                                                                face.return_code,
                                                                                                face.message,
                                                                                                face.age,
                                                                                                face.bounding_box.top_left_coordinate.__str__(),
                                                                                                face.bounding_box.bottom_right_coordinate.__str__()))
    if len(is_valid_handle.face_objects) == 0:
        print("No Faces found!!\n")


if __name__ == "__main__":
    images_files_path = str(pathlib.Path(__file__).parent.joinpath("example/test_images/").resolve())
    image_file_list = []
    image_file_list.extend(glob("{}/*.png".format(images_files_path)))
    image_file_list.extend(sorted(glob("{}/*.jpg".format(images_files_path))))
    image_file_list.extend(sorted(glob("{}/*.jpeg".format(images_files_path))))

    config_object = ConfigObject(
        config_param={PARAMETERS.INPUT_IMAGE_FORMAT: "rgb",
                      PARAMETERS.CONTEXT_STRING: "predict"})
    # print(config_object.get_config_param())

    face_factor = FaceFactor(logging_level=LoggingLevel.off, config=config_object)
    # face_factor.update_config(config=config_object)

    for img_path in image_file_list:
        print(colored("\nImage:{}\n".format(img_path), "red"))
        test_valid(face_factor, img_path)
        test_valid(face_factor, img_path, config=config_object)
        test_age_estimate(face_factor, img_path)
        test_age_estimate(face_factor, img_path, config=config_object)
        # test_compare(face_factor, img_path)
        # test_enroll(face_factor, img_path)
        # result_handle = test_predict(face_factor, img_path)
        # test_delete(face_factor, result_handle)

import pathlib
import sys
import os
from timeit import default_timer
import os
from PIL import Image
from termcolor import colored

src_path = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(src_path))
import numpy as np
from src.cryptonets_python_sdk.settings.configuration import ConfigObject
from src.cryptonets_python_sdk.settings.configuration import PARAMETERS
from src.cryptonets_python_sdk.factor import FaceFactor
from src.cryptonets_python_sdk.settings.loggingLevel import LoggingLevel
from src.cryptonets_python_sdk.settings.cacheType import CacheType


def image_path_to_array(image_path: str) -> np.ndarray:
    image = Image.open(image_path).convert("RGB")
    return np.array(image)


def test_compare(compare_face_factor, compare_path, config=None):
    print(colored("{}\n{}".format("Compare", "=" * 25), "green"))
    compare_start_time = default_timer()
    compare_handle = compare_face_factor.compare(
        image_path_1=compare_path,
        image_path_2=build_sample_image_path("18.jpg"),
        config=config,
    )
    print("Duration:", default_timer() - compare_start_time, "\n")
    print(
        "Status:{}\nResult:{}\nMessage:{}\nMin:{}\nMean:{}\nMax:{}\n1VR:{}\n2VR:{}\n".format(
            compare_handle.status,
            compare_handle.result,
            compare_handle.message,
            compare_handle.distance_min,
            compare_handle.distance_mean,
            compare_handle.distance_max,
            compare_handle.first_validation_result,
            compare_handle.second_validation_result,
        )
    )


def test_predict(predict_face_factor, predict_img_path, config=None):
    print(colored("{}\n{}".format("Predict", "=" * 25), "green"))
    predict_start_time = default_timer()
    predict_handle = predict_face_factor.predict(
        image_path=predict_img_path, config=config
    )
    print("Duration:", default_timer() - predict_start_time, "\n")
    print(
        "Status:{}\nMessage:{}\nEnroll Level:{}\nPUID:{}\nGUID:{}\nToken:{}\n".format(
            predict_handle.status,
            predict_handle.message,
            predict_handle.enroll_level,
            predict_handle.puid,
            predict_handle.guid,
            predict_handle.token,
        )
    )
    return predict_handle


def test_enroll(enroll_face_factor, enroll_img_path, config=None):
    print(colored("{}\n{}".format("Enroll", "=" * 25), "green"))
    enroll_start_time = default_timer()
    enroll_handle = enroll_face_factor.enroll(image_path=enroll_img_path, config=config)
    print("Duration:", default_timer() - enroll_start_time, "\n")
    print(
        "Status:{}\nMessage:{}\nEnroll Level:{}\nPUID:{}\nGUID:{}\nToken:{}\n".format(
            enroll_handle.status,
            enroll_handle.message,
            enroll_handle.enroll_level,
            enroll_handle.puid,
            enroll_handle.guid,
            enroll_handle.token,
        )
    )


def test_delete(delete_face_factor, predict_handle):
    print(colored("{}\n{}".format("Delete", "=" * 25), "green"))
    delete_start_time = default_timer()
    print(predict_handle.puid)
    delete_handle = delete_face_factor.delete(predict_handle.puid)
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
            "Face#:{}\n{}\nReturn Code:{}\nMessage:{}\nAge:{}\nBBox TL:{}\nBBox BR:{}\n".format(
                index + 1,
                "-" * 7,
                face.return_code,
                face.message,
                face.age,
                face.bounding_box.top_left_coordinate.__str__(),
                face.bounding_box.bottom_right_coordinate.__str__(),
            )
        )

    if len(age_handle.face_objects) == 0:
        print("No Faces found!!\n")


def test_get_iso_face(get_iso_face_factor, age_path, config=None):
    print(colored("{}\n{}".format("Get ISO FACE", "=" * 25), "green"))
    start_time = default_timer()
    get_iso_face_handle = get_iso_face_factor.get_iso_face(
        image_path=age_path, config=config
    )
    print("Duration:", default_timer() - start_time, "\n")
    print(
        "Status:{}\nMessage:{}\nISO_image_width:{}\nISO_image_height: {}\nISO_image_channels:{}\nConfidence:{} ".format(
            get_iso_face_handle.status,
            get_iso_face_handle.message,
            get_iso_face_handle.iso_image_width,
            get_iso_face_handle.iso_image_height,
            get_iso_face_handle.iso_image_channels,
            get_iso_face_handle.confidence,
        )
    )

    if get_iso_face_handle.image:
        get_iso_face_handle.image.show()


def test_valid(valid_face_factor, valid_path, config=None):
    print(colored("{}\n{}".format("Is Valid", "=" * 25), "green"))
    valid_start_time = default_timer()
    is_valid_handle = valid_face_factor.is_valid(image_path=valid_path, config=config)
    print("Duration:", default_timer() - valid_start_time, "\n")

    print("Error:{}\nMessage:{}".format(is_valid_handle.error, is_valid_handle.message))
    for index, face in enumerate(is_valid_handle.face_objects):
        print(
            "Face#:{}\n{}\nReturn Code:{}\nMessage:{}\nAge:{}\nBBox TL:{}\nBBox BR:{}\n".format(
                index + 1,
                "-" * 7,
                face.return_code,
                face.message,
                face.age,
                face.bounding_box.top_left_coordinate.__str__(),
                face.bounding_box.bottom_right_coordinate.__str__(),
            )
        )
    if len(is_valid_handle.face_objects) == 0:
        print("No Faces found!!\n")


def build_sample_image_path(image_filename=None):
    images_files_path = str(
        pathlib.Path(__file__).parent.joinpath("example/test_images/").resolve()
    )
    image_file_path = "{}/{}".format(images_files_path, image_filename)
    return image_file_path


def setup_test(
    image_filename=None,
    operation_threshold_parameter_name=None,
    threshold_value=0,
    use_cache=False,
    call_context="predict",
):
    image_file_path = build_sample_image_path(image_filename)
    config_param = {
        PARAMETERS.INPUT_IMAGE_FORMAT: "rgb",
        PARAMETERS.CONTEXT_STRING: call_context,
    }
    if operation_threshold_parameter_name is not None:
        config_param[operation_threshold_parameter_name] = threshold_value
    config_object = ConfigObject(config_param)

    a_cache_type = CacheType.ON if use_cache is False else CacheType.ON

    face_factor = FaceFactor(
        logging_level=LoggingLevel.off,config=config_object
    )

    return face_factor, image_file_path


def setup_compare_test(
    image1_filename=None,
    image2_filename=None,
    operation_threshold_parameter_name=None,
    threshold_value=0,
    use_cache=False,
    call_context="predict",
):
    image1_file_path = build_sample_image_path(image1_filename)
    image2_file_path = build_sample_image_path(image2_filename)
    config_param = {
        PARAMETERS.INPUT_IMAGE_FORMAT: "rgb",
        PARAMETERS.CONTEXT_STRING: call_context,
    }
    if operation_threshold_parameter_name is not None:
        config_param[operation_threshold_parameter_name] = threshold_value
    config_object = ConfigObject(config_param)

    a_cache_type = CacheType.ON if use_cache is False else CacheType.ON

    face_factor = FaceFactor(
        logging_level=LoggingLevel.off, config=config_object, cache_type=a_cache_type
    )

    return face_factor, image1_file_path, image2_file_path


def test_predict_enrol_valid_image_with_cache():
    # Notice we do not need to pass enroll reservation qty
    (face_factor, image_path) = setup_test("8.png", use_cache=True)
    test_enroll(face_factor, image_path)  # => no billing reservation
    result_handle = test_predict(face_factor, image_path)  # =>  no billing reservation
    result_handle = test_predict(face_factor, image_path)  # => no billing reservation
    result_handle = test_predict(face_factor, image_path)  # => no billing reservation
    test_delete(face_factor, result_handle)  # => no billing for delete
    result_handle = test_predict(face_factor, image_path)  # => no billing reservation
    test_delete(face_factor, result_handle)  # => no billing for delete
    result_handle = test_predict(face_factor, image_path)  # => no billing reservation
    test_delete(face_factor, result_handle)  # => no billing for delete


def test_predict_enrol_valid_image_with_no_cache():
    # Notice we do not need to pass enroll reservation qty
    (face_factor, image_path) = setup_test("8.png")
    test_enroll(face_factor, image_path)  # => no billing reservation
    result_handle = test_predict(face_factor, image_path)  # => no billing reservation
    result_handle = test_predict(face_factor, image_path)  # => no billing reservation
    result_handle = test_predict(face_factor, image_path)  # => no billing reservation
    test_delete(face_factor, result_handle)  # => no billing for delete
    result_handle = test_predict(face_factor, image_path)  # => no billing reservation
    test_delete(face_factor, result_handle)  # => no billing for delete
    result_handle = test_predict(face_factor, image_path)  # => no billing reservation
    result_handle = test_predict(face_factor, image_path)  # => no billing reservation
    test_delete(face_factor, result_handle)  # => no billing for delete


def test_valid_with_cache():
    (face_factor, image_path) = setup_test("8.png", use_cache=True)
    test_valid(face_factor, image_path)  # => no billing
    test_valid(face_factor, image_path)  # => no billing
    test_valid(face_factor, image_path)  # => no billing
    test_valid(face_factor, image_path)  # => no billing


def test_valid_with_bad_image_and_no_cache():
    (face_factor, image_path) = setup_test("5.png", use_cache=False)
    test_valid(face_factor, image_path)  # => no billing
    test_valid(face_factor, build_sample_image_path("6.png"))  # => no billing
    test_valid(face_factor, build_sample_image_path("8.png"))  # => no billing
    test_valid(face_factor, build_sample_image_path("6.png"))  # => no billing
    test_valid(face_factor, build_sample_image_path("6.png"))  # => no billing


def test_age_estimate_with_cache():
    (face_factor, image_path) = setup_test(
        "5.png", PARAMETERS.ESTIMATE_AGE_RESERVATION_CALLS, 2, True
    )
    test_age_estimate(
        face_factor, image_path
    )  # => no billing for invalid age => tested OK
    test_age_estimate(
        face_factor, build_sample_image_path("6.png")
    )  # => no billing for invalid age
    test_age_estimate(
        face_factor, build_sample_image_path("8.png")
    )  # => billing reservation of 2 and local bill increment (1)
    test_age_estimate(
        face_factor, build_sample_image_path("6.png")
    )  # => no billing for invalid age
    test_age_estimate(
        face_factor, build_sample_image_path("6.png")
    )  # => no billing for invalid age
    test_age_estimate(
        face_factor, build_sample_image_path("8.png")
    )  # => local bill increment (2)


def test_age_estimate_with_no_cache():
    (face_factor, image_path) = setup_test(
        "5.png", PARAMETERS.ESTIMATE_AGE_RESERVATION_CALLS, 2
    )
    test_age_estimate(
        face_factor, image_path
    )  # => no billing for invalid age => tested OK
    test_age_estimate(
        face_factor, build_sample_image_path("6.png")
    )  # => no billing for invalid age
    test_age_estimate(
        face_factor, build_sample_image_path("8.png")
    )  # => billing reservation of 2 and local bill increment (1)
    test_age_estimate(
        face_factor, build_sample_image_path("6.png")
    )  # => no billing for invalid age
    test_age_estimate(
        face_factor, build_sample_image_path("6.png")
    )  # => no billing for invalid age
    test_age_estimate(
        face_factor, build_sample_image_path("8.png")
    )  # => local bill increment (2)
    test_age_estimate(
        face_factor, build_sample_image_path("8.png")
    )  # => billing reservation of 2 and local bill increment (1)


def test_compare_with_cache():
    (face_factor, image_path) = setup_test(
        "8.png", PARAMETERS.COMPARE_RESERVATION_CALLS, 2, True
    )
    test_compare(
        face_factor, image_path
    )  # => billing reservation of 2 and local bill increment (1)
    test_compare(face_factor, image_path)  # => local bill increment (2)
    test_compare(
        face_factor, image_path
    )  # => billing reservation of 2 and local bill increment (1)
    test_compare(
        face_factor, build_sample_image_path("6.png")
    )  # => local bill increment (2)
    test_compare(
        face_factor, build_sample_image_path("6.png")
    )  # => billing reservation of 2 and local bill increment (1)


def test_compare_with_no_cache():
    (face_factor, image_path) = setup_test(
        "8.png", PARAMETERS.COMPARE_RESERVATION_CALLS, 2
    )
    test_compare(
        face_factor, image_path
    )  # => billing reservation of 2 and local bill increment (1)
    test_compare(face_factor, image_path)  # => local bill increment (2)
    test_compare(
        face_factor, image_path
    )  # => billing reservation of 2 and local bill increment (1)
    # test_compare(face_factor, build_sample_image_path("6.png"))  # => local bill increment (2)
    # test_compare(face_factor,
    #              build_sample_image_path("6.png"))  # => billing reservation of 2 and local bill increment (1)


def test_get_iso_image_with_cache():
    (face_factor, image_path) = setup_test(
        "8.png", PARAMETERS.FACE_ISO_RESERVATION_CALLS, 2, True
    )
    test_get_iso_face(face_factor, image_path)  # no billing reservation
    test_get_iso_face(face_factor, image_path)  # no billing reservation
    test_get_iso_face(
        face_factor, build_sample_image_path("6.png")
    )  # no billing reservation


def test_get_iso_image_with_no_cache():
    (face_factor, image_path) = setup_test(
        "8.png", PARAMETERS.FACE_ISO_RESERVATION_CALLS, 2
    )
    test_get_iso_face(face_factor, image_path)  # no billing reservation
    test_get_iso_face(face_factor, image_path)  # no billing reservation
    test_get_iso_face(
        face_factor, build_sample_image_path("6.png")
    )  # no billing reservation

def get_image_paths(folder_path):
    """
    Returns a list of paths for all image files in the specified folder.
    Supported image formats: jpg, jpeg, png, gif, bmp
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    image_paths = [os.path.join(folder_path, file) 
                   for file in os.listdir(folder_path) 
                   if os.path.splitext(file)[1].lower() in image_extensions]
    return image_paths
if __name__ == "__main__":
    os.environ["PI_SERVER_URL"] = "https://api.prodv2.cryptonets.ai/node"
    os.environ["PI_API_KEY"] = "00000000000000001962"
   
    (face_factor, image_path_1,) = setup_test(
        "test.jpeg",
    )
    # (face_factor, img1, img2) = setup_compare_test(
    #     "3_predict_cropped_images_0.png", "8.png"
    # )
    # (face_factor, img1, img2) = setup_compare_test("8.png", "8.png")
    # test_enroll(face_factor, image_path)  # => no billing reservation
    # result_handle = test_predict(face_factor, image_path) # => no billing reservation

    # test_delete(face_factor, result_handle) # => no billing for delete
    # result_handle = test_predict(face_factor, image_path)  # => no billing reservation
    # test_delete(face_factor, result_handle)
    # test_predict_enrol_valid_image_with_no_cache()
    # test_valid_with_cache()
    # test_valid(face_factor, "/home/azam/projects/openinfer/python sdk/cryptonets-python-sdk/docs/source/Usage/images/johny.jpg")
    # test_age_estimate(face_factor, "/home/azam/projects/openinfer/python sdk/cryptonets-python-sdk/tests/example/test_images/12.jpeg")
    # for image_path in get_image_paths("/home/azam/projects/openinfer/python sdk/cryptonets-python-sdk/tests/example/test_images"):
    #     print(image_path)
    #     test_age_estimate(face_factor, image_path)
        

    # test_age_estimate_with_no_cache()
    compare_start_time = default_timer()
    compare_handle = face_factor.compare(image_path_1="/home/azam/projects/openinfer/python sdk/cryptonets-python-sdk/docs/source/Usage/images/tom_hanks.png",image_path_2="/home/azam/projects/openinfer/python sdk/cryptonets-python-sdk/docs/source/Usage/images/tom_hanks_2.jpg")
    print("Duration:", default_timer() - compare_start_time, "\n")
    print("Status:{}\nResult:{}\nMessage:{}\nMin:{}\nMean:{}\nMax:{}\n1VR:{}\n2VR:{}\n".format(
        compare_handle.status,
        compare_handle.result, compare_handle.message, compare_handle.distance_min,
        compare_handle.distance_mean,
        compare_handle.distance_max, compare_handle.first_validation_result,
        compare_handle.second_validation_result))
    # test_compare_with_no_cache()
    # test_get_iso_image_with_cache()
    # test_get_iso_image_with_no_cache()
    # print("Done")
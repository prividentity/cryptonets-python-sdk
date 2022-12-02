import glob
import pathlib
import sys
from timeit import default_timer

from PIL import Image
from termcolor import colored

src_path = pathlib.Path(__file__).parent.parent.resolve()
sys.path.append(str(src_path))
import numpy as np
from src.cryptonets_python_sdk.factor import FaceFactor
from src.cryptonets_python_sdk.settings.loggingLevel import LoggingLevel


def image_path_to_array(image_path: str) -> np.ndarray:
    image = Image.open(image_path).convert('RGB')
    return np.array(image)


images_files_path = str(pathlib.Path(__file__).parent.joinpath("example/test_images/").resolve())
imagesfiles = []
imagesfiles.extend(glob.glob("{}/*.png".format(images_files_path)))
imagesfiles.extend(sorted(glob.glob("{}/*.jpg".format(images_files_path))))
imagesfiles.extend(sorted(glob.glob("{}/*.jpeg".format(images_files_path))))

SERVER_URL = ""
api_key = ""

if __name__ == "__main__":
    face_factor = FaceFactor(
        server_url=SERVER_URL, api_key=api_key,
        logging_level=LoggingLevel.off.value)
    for img_path in imagesfiles:
        print(colored("\nImage:{}\n".format(img_path), "red"))

        print(colored("{}\n{}".format("Is Valid", "=" * 25), "green"))
        start_time = default_timer()
        is_valid_handle = face_factor.is_valid(image_path=img_path)
        print("Duration:", default_timer() - start_time, "\n")

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

        print(colored("{}\n{}".format("Age Estimation", "=" * 25), "green"))
        start_time = default_timer()
        age_handle = face_factor.estimate_age(image_path=img_path)
        print("Duration:", default_timer() - start_time, "\n")
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

        # print(colored("{}\n{}".format("Compare", "=" * 25), "green"))
        # start_time = default_timer()
        # compare_handle = face_factor.compare(image_path_1=img_path, image_path_2=img_path)
        # print("Duration:", default_timer() - start_time, "\n")
        # print("Status:{}\nResult:{}\nMessage:{}\nMin:{}\nMean:{}\nMax:{}\n1VR:{}\n2VR:{}\n".format(
        #     compare_handle.status,
        #     compare_handle.result, compare_handle.message, compare_handle.distance_min,
        #     compare_handle.distance_mean,
        #     compare_handle.distance_max, compare_handle.first_validation_result,
        #     compare_handle.second_validation_result))
        #
        # print(colored("{}\n{}".format("Enroll", "=" * 25), "green"))
        # start_time = default_timer()
        # enroll_handle = face_factor.enroll(image_path=img_path)
        # print("Duration:", default_timer() - start_time, "\n")
        # print("Status:{}\nMessage:{}\nEnroll Level:{}\nUUID:{}\nGUID:{}\nToken:{}\n".format(enroll_handle.status,
        #                                                                                     enroll_handle.message,
        #                                                                                     enroll_handle.enroll_level,
        #                                                                                     enroll_handle.uuid,
        #                                                                                     enroll_handle.guid,
        #                                                                                     enroll_handle.token))
        #
        # print(colored("{}\n{}".format("Predict", "=" * 25), "green"))
        # start_time = default_timer()
        # predict_handle = face_factor.predict(image_path=img_path)
        # print("Duration:", default_timer() - start_time, "\n")
        # print("Status:{}\nMessage:{}\nEnroll Level:{}\nUUID:{}\nGUID:{}\nToken:{}\n".format(predict_handle.status,
        #                                                                                     predict_handle.message,
        #                                                                                     predict_handle.enroll_level,
        #                                                                                     predict_handle.uuid,
        #                                                                                     predict_handle.guid,
        #                                                                                     predict_handle.token))
        #
        # print(colored("{}\n{}".format("Delete", "=" * 25), "green"))
        # start_time = default_timer()
        # delete_handle = face_factor.delete(predict_handle.uuid)
        # print("Duration:", default_timer() - start_time, "\n")
        # print("Status:{}\nMessage:{}".format(delete_handle.status, delete_handle.message))

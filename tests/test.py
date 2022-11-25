import pathlib
import sys
from PIL import Image
import glob

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
        logging_level=LoggingLevel.full.value)
    for img_path in imagesfiles:
        print("...........Performing operations for image {} : ...........\n", img_path)
        ## By Image Path
        print("...........Calling functions by using image path  : ...........\n")
        print("...........Calling isvalid : ...........\n")
        is_valid_handle = face_factor.is_valid(image_path=img_path)
        print("Is_valid=>Status:{}, Message:{}".format(is_valid_handle.status, is_valid_handle.message))
        print("........... isvalid completed ...........\n\n")

        print("...........Calling estimate_age: ...........\n")
        age_handle = face_factor.estimate_age(image_path=img_path)
        print("estimate_age=>Status:{} , Age:{}, Message:{}".format(age_handle.status, age_handle.age,
                                                                    age_handle.message))
        print("........... estimate_age completed ...........\n\n")
        print("........... Calling Compare : ...........\n")
        compare_handle = face_factor.compare(image_path_1=img_path, image_path_2=img_path)
        print("Compare=>Status:{}, Result:{}, Message:{}, Min:{}, Mean:{}, Max:{}, 1VR:{}, 2VR:{}".format(
            compare_handle.status,
            compare_handle.result, compare_handle.message, compare_handle.distance_min, compare_handle.distance_mean,
            compare_handle.distance_max, compare_handle.first_validation_result,
            compare_handle.second_validation_result))
        print("........... Compare completed ...........\n\n")

        print("........... Calling Enroll : ...........\n")
        enroll_handle = face_factor.enroll(image_path=img_path)
        print("Enroll=>Status:{}, Message:{}, Enroll Level:{}, UUID:{}, GUID:{}, Token:{}".format(enroll_handle.status,
                                                                                                  enroll_handle.message,
                                                                                                  enroll_handle.enroll_level,
                                                                                                  enroll_handle.uuid,
                                                                                                  enroll_handle.guid,
                                                                                                  enroll_handle.token))
        print("........... Enroll Completed : ...........\n\n")

        print("........... Calling Predict : ...........\n")
        predict_handle = face_factor.predict(image_path=img_path)
        print(
            "Predict=>Status:{}, Message:{}, Enroll Level:{}, UUID:{}, GUID:{}, Token:{}".format(predict_handle.status,
                                                                                                 predict_handle.message,
                                                                                                 predict_handle.enroll_level,
                                                                                                 predict_handle.uuid,
                                                                                                 predict_handle.guid,
                                                                                                 predict_handle.token))
        print("........... Predict Completed : ...........\n\n")
        print("...........  Calling Delete for uuid:\n", predict_handle.uuid)
        delete_handle = face_factor.delete(predict_handle.uuid)
        print("Delete=>Status:{}, Message:{}".format(delete_handle.status, delete_handle.message))
        print("........... Delete completed : ...........\n\n")

        ## By PIL Image
        # print("...........Calling functions by using image data  : ...........\n")
        # print("...........Calling isvalid : ...........\n")
        # is_valid_handle = face_factor.is_valid(image_data=img_data)
        # print("Is_valid=>Status:{}, Message:{}".format(is_valid_handle.status, is_valid_handle.message))
        # print("........... isvalid completed ...........\n\n")

        # print("........... Calling Compare : ...........\n")
        # compare_handle = face_factor.compare(image_data_1=img_data, image_data_2=img_data)
        # print("Compare=>Status:{}, Result:{}, Message:{}, Min:{}, Mean:{}, Max:{}, 1VR:{}, 2VR:{}".format(
        #     compare_handle.status,
        #     compare_handle.result, compare_handle.message, compare_handle.distance_min, compare_handle.distance_mean,
        #     compare_handle.distance_max, compare_handle.first_validation_result, compare_handle.second_validation_result))
        # print("........... Compare completed ...........\n\n")

        # print("........... Calling Enroll : ...........\n")
        # enroll_handle = face_factor.enroll(image_data=img_data)
        # print("Enroll=>Status:{}, Message:{}, Enroll Level:{}, UUID:{}, GUID:{}, Token:{}".format(enroll_handle.status,
        #                                                                                         enroll_handle.message,
        #                                                                                         enroll_handle.enroll_level,
        #                                                                                         enroll_handle.uuid,
        #                                                                                         enroll_handle.guid,
        #                                                                                         enroll_handle.token))
        # print("........... Enroll Completed : ...........\n\n")

        # print("........... Calling Predict : ...........\n")
        # predict_handle = face_factor.predict(image_data=img_data)
        # print("Predict=>Status:{}, Message:{}, Enroll Level:{}, UUID:{}, GUID:{}, Token:{}".format(enroll_handle.status,
        #                                                                                         enroll_handle.message,
        #                                                                                         enroll_handle.enroll_level,
        #                                                                                         enroll_handle.uuid,
        #                                                                                         enroll_handle.guid,
        #                                                                                         enroll_handle.token))
        # print("........... Predict Completed : ...........\n\n")

        # print("...........  Calling Delete for uuid:\n", predict_handle.uuid)
        # delete_handle = face_factor.delete(predict_handle.uuid)
        # print("Delete=>Status:{}, Message:{}".format(delete_handle.status, delete_handle.message))
        # print("........... Delete completed : ...........\n\n")
        print("........... Completed Performing operations for image {} : ...........\n", img_path)
        pass

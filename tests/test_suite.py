import sys
from glob import glob
from pathlib import Path

import pytest

import dataResult

src_path = Path(__file__).parent.parent.resolve()
sys.path.append(str(src_path))

from src.cryptonets_python_sdk.factor import FaceFactor
from src.cryptonets_python_sdk.settings.cacheType import CacheType
from src.cryptonets_python_sdk.settings.configuration import ConfigObject, PARAMETERS
from src.cryptonets_python_sdk.settings.loggingLevel import LoggingLevel


class ParametersSetup:
    def __init__(self):
        self.file_list = None
        self.dataResult = dataResult
        self.is_valid_params = []
        self.estimate_age_params = []
        self.get_iso_params = []
        self.compare_params = []
        self.epd_params = []
        self.populate_file_list()
        self.populate_params()

    def populate_file_list(self):
        images_files_path = str(
            Path(__file__).parent.joinpath("example/test_images/").resolve()
        )
        self.file_list = []
        self.file_list.extend(glob("{}/*.png".format(images_files_path)))
        self.file_list.extend(sorted(glob("{}/*.jpg".format(images_files_path))))
        self.file_list.extend(sorted(glob("{}/*.jpeg".format(images_files_path))))

    def populate_params(self):
        for file_path in self.file_list:
            posix_path = Path(file_path)
            self.is_valid_params.append(
                (
                    "factor_object",
                    file_path,
                    eval(
                        "dataResult.{}().is_valid_result".format(
                            posix_path.suffix[1:].capitalize() + posix_path.stem
                        )
                    ),
                )
            )
            self.estimate_age_params.append(
                (
                    "factor_object",
                    file_path,
                    eval(
                        "dataResult.{}().estimate_age_result".format(
                            posix_path.suffix[1:].capitalize() + posix_path.stem
                        )
                    ),
                )
            )
            self.get_iso_params.append(
                (
                    "factor_object",
                    file_path,
                    eval(
                        "dataResult.{}().get_iso_result".format(
                            posix_path.suffix[1:].capitalize() + posix_path.stem
                        )
                    ),
                )
            )
            self.compare_params.append(
                (
                    "factor_object",
                    file_path,
                    eval(
                        "dataResult.{}().compare_result".format(
                            posix_path.suffix[1:].capitalize() + posix_path.stem
                        )
                    ),
                )
            )
            self.epd_params.append(
                (
                    "factor_object",
                    file_path,
                    eval(
                        "dataResult.{}().enroll_result".format(
                            posix_path.suffix[1:].capitalize() + posix_path.stem
                        )
                    ),
                    eval(
                        "dataResult.{}().predict_result".format(
                            posix_path.suffix[1:].capitalize() + posix_path.stem
                        )
                    ),
                    eval(
                        "dataResult.{}().delete_result".format(
                            posix_path.suffix[1:].capitalize() + posix_path.stem
                        )
                    ),
                )
            )


@pytest.fixture(scope="session")
def factor_object():
    config_object = ConfigObject(
        config_param={
            PARAMETERS.INPUT_IMAGE_FORMAT: "rgb",
            PARAMETERS.CONTEXT_STRING: "predict",
            PARAMETERS.ESTIMATE_AGE_RESERVATION_CALLS: 10,
        }
    )
    face_factor = FaceFactor(
        logging_level=LoggingLevel.off, config=config_object, cache_type=CacheType.OFF
    )
    return face_factor


@pytest.mark.parametrize(
    "factor_object, file_name, expected",
    ParametersSetup().is_valid_params,
    indirect=["factor_object"],
)
def test_valid(factor_object, file_name, expected):
    actual = factor_object.is_valid(file_name)
    assert expected.error == actual.error
    assert expected.message == actual.message
    assert len(expected.face_objects) == len(actual.face_objects)
    for expected, actual in zip(
        sorted(
            expected.face_objects, key=lambda x: x.bounding_box.top_left_coordinate.x
        ),
        sorted(actual.face_objects, key=lambda x: x.bounding_box.top_left_coordinate.x),
    ):
        assert actual.return_code == expected.return_code
        assert actual.message == expected.message
        assert actual.age == expected.age
        assert (
            actual.bounding_box.top_left_coordinate.__str__()
            == expected.bounding_box.top_left_coordinate.__str__()
        )
        assert (
            actual.bounding_box.bottom_right_coordinate.__str__()
            == expected.bounding_box.bottom_right_coordinate.__str__()
        )


@pytest.mark.parametrize(
    "factor_object, file_name, expected",
    ParametersSetup().estimate_age_params,
    indirect=["factor_object"],
)
def test_estimate_age(factor_object, file_name, expected):
    actual = factor_object.estimate_age(file_name)
    assert expected.error == actual.error
    assert expected.message == actual.message
    assert len(expected.face_objects) == len(actual.face_objects)
    for expected, actual in zip(
        sorted(
            expected.face_objects, key=lambda x: x.bounding_box.top_left_coordinate.x
        ),
        sorted(actual.face_objects, key=lambda x: x.bounding_box.top_left_coordinate.x),
    ):
        assert actual.return_code == expected.return_code
        assert actual.message == expected.message
        if actual.age is None:
            assert actual.age == expected.age
        else:
            assert expected.age - 0.5 <= actual.age <= expected.age + 0.5
        assert (
            actual.bounding_box.top_left_coordinate.__str__()
            == expected.bounding_box.top_left_coordinate.__str__()
        )
        assert (
            actual.bounding_box.bottom_right_coordinate.__str__()
            == expected.bounding_box.bottom_right_coordinate.__str__()
        )


@pytest.mark.parametrize(
    "factor_object, file_name, expected",
    ParametersSetup().get_iso_params,
    indirect=["factor_object"],
)
def test_get_iso(factor_object, file_name, expected):
    actual = factor_object.get_iso_face(file_name)
    assert expected.status == actual.status
    assert expected.message == actual.message
    assert expected.iso_image_height == actual.iso_image_height
    assert expected.iso_image_width == actual.iso_image_width
    assert expected.iso_image_channels == actual.iso_image_channels
    if actual.confidence is None:
        assert actual.confidence == expected.confidence
    else:
        assert (
            expected.confidence - 0.5 <= actual.confidence <= expected.confidence + 0.5
        )


@pytest.mark.parametrize(
    "factor_object, file_name, expected",
    ParametersSetup().compare_params,
    indirect=["factor_object"],
)
def test_compare(factor_object, file_name, expected):
    actual = factor_object.compare(image_path_1=file_name, image_path_2=file_name)
    assert expected.status == actual.status
    assert expected.result == actual.result
    assert expected.message == actual.message
    assert expected.first_validation_result == actual.first_validation_result
    assert expected.second_validation_result == actual.second_validation_result


@pytest.mark.parametrize(
    "factor_object, file_name, enroll_expected, predict_expected, delete_expected",
    ParametersSetup().epd_params,
    indirect=["factor_object"],
)
def test_epd(
    factor_object, file_name, enroll_expected, predict_expected, delete_expected
):
    enroll_actual = factor_object.enroll(file_name)
    assert enroll_expected.status == enroll_actual.status
    predict_actual = factor_object.predict(file_name)
    assert predict_expected.status == predict_actual.status
    assert predict_expected.message.lower() == predict_actual.message.lower()
    if predict_expected.enroll_level is None:
        assert predict_expected.enroll_level == predict_actual.enroll_level
    else:
        assert enroll_actual.enroll_level == predict_actual.enroll_level
        assert enroll_actual.puid == predict_actual.puid
        assert enroll_actual.guid == predict_actual.guid
    if enroll_actual.puid is not None:
        actual = factor_object.delete(enroll_actual.puid)
        assert delete_expected.status == actual.status
        assert delete_expected.message.lower() == actual.message.lower()

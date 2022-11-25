from PIL import Image
import numpy as np
from enum import Enum, EnumMeta


def image_path_to_array(image_path: str) -> np.ndarray:
    image = Image.open(image_path).convert('RGB')
    return np.array(image)


class FaceValidationCodeMeta(EnumMeta):
    def __contains__(cls, item):
        return item in [v.value for v in cls.__members__.values()]


class FaceValidationCode(Enum, metaclass=FaceValidationCodeMeta):
    InvalidImage = -100
    NoFace = -1
    ValidBiometric = 0
    ImageSpoof = 1
    VideoSpoof = 2
    TooClose = 3
    TooFaraway = 4
    TooFarToRight = 5
    TooFarToLeft = 6
    TooFarUp = 7
    TooFarDown = 8
    TooBlurry = 9
    GlassesOn = 10
    MaskOn = 11
    ChinTooFarLeft = 12
    ChinTooFarRight = 13
    ChinTooFarUp = 14
    ChinTooFarDown = 15

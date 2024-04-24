from enum import Enum, EnumMeta

import numpy as np
from PIL import Image
import os

import exifread


def get_exif_orientation(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f)
    # Exifread uses 'Image Orientation' to store the orientation data
    orientation_tag = 'Image Orientation'
    if orientation_tag in tags:
        # Convert the value to an integer
        orientation_value = tags[orientation_tag].values[0]
        # Return the orientation value
        return orientation_value
    else:
        # No orientation tag found, return a default value
        return 1
def apply_rotation(image, orientation):
    """
    Applies rotation to the image based on the EXIF orientation.
    """
    if orientation == 3:
        image = image.rotate(180, expand=True)
    elif orientation == 6:
        image = image.rotate(270, expand=True)
    elif orientation == 8:
        image = image.rotate(90, expand=True)

    return image

def image_path_to_array(image_path: str, input_format: str) -> np.ndarray:
    image = Image.open(image_path).convert(input_format.upper())
    image=apply_rotation(image,get_exif_orientation(image_path))
    return np.array(image)


class Point(object):
    """Creates a point on a coordinate plane with values x and y.
    """

    def __init__(self, x=None, y=None):
        """
        Point object having the x and y coordinates
        """
        self._x = x
        self._y = y

    @property
    def x(self):
        """
        Returns the x coordinate of the object
        """
        return self._x

    @property
    def y(self):
        """
        Returns the y coordinate of the object
        """
        return self._y

    def __str__(self):
        return "Point(%s,%s)" % (self._x, self._y)


class BoundingBox(object):
    def __init__(self, top_left_coordinate=None, bottom_right_coordinate=None):
        """
        Bounding box class for capturing the coordinates of the detected image
        """
        self._bottom_right_coordinate = Point(None, None)
        self._top_left_coordinate = Point(None, None)
        if bottom_right_coordinate:
            self._bottom_right_coordinate = Point(
                bottom_right_coordinate.get("x", None),
                bottom_right_coordinate.get("y", None),
            )
        if top_left_coordinate:
            self._top_left_coordinate = Point(
                top_left_coordinate.get("x", None), top_left_coordinate.get("y", None)
            )

    @property
    def bottom_right_coordinate(self) -> Point:
        """
        Returns the bottom right coordinate

        Returns
        -------
        Point
            x: float

            y: float

        """
        return self._bottom_right_coordinate

    @property
    def top_left_coordinate(self) -> Point:
        """
        Returns the top left coordinate

        Returns
        -------
        Point
            x: float

            y: float

        """
        return self._top_left_coordinate

    @bottom_right_coordinate.setter
    def bottom_right_coordinate(self, value):
        self._bottom_right_coordinate = value

    @top_left_coordinate.setter
    def top_left_coordinate(self, value):
        self._top_left_coordinate = value


class FaceValidationCodeMeta(EnumMeta):
    def __contains__(cls, item):
        return item in [v.value for v in cls.__members__.values()]


class FaceValidationCode(Enum, metaclass=FaceValidationCodeMeta):
    InvalidImage = -100  # Err = -100
    NoFace = -1  # faceNotDetected = -1
    ValidBiometric = 0  # Ok = 0
    ImageSpoof =  1

    VideoSpoof = 2 
    TooClose = 3  # faceTooClose = 3
    TooFaraway = 4  # faceTooFar = 4
    TooFarToRight = 5  # faceRight = 5
    TooFarToLeft = 6  # faceLeft = 6
    TooFarUp = 7  # faceUp = 7
    TooFarDown = 8  # faceDown = 8
    TooBlurry = 9  # imageBlurr = 9
    GlassesOn = 10  # faceWithGlass = 10
    MaskOn = 11  # faceWithMask = 11
    ChinTooFarLeft = 12  # lookingLeft = 12
    ChinTooFarRight = 13  # lookingRight = 13
    ChinTooFarUp = 14  # lookingHigh = 14
    ChinTooFarDown = 15  # lookingDown = 15
    FaceTooDark = 16  # FaceTooDark = 16
    FaceTooBright = 17  # FaceTooBright = 17
    FaceLowValConf = 18  # FaceLowValConf = 18
    InvalidFaceBackground = 19  # InvalidFaceBackground = 19
    EyeBlink = 20  # EyeBlink = 20
    МouthOpened = 21  # МouthOpened = 21
    faceRotatedRight = 22
    faceRotatedLeft = 23

    
from ..utils import BoundingBox


class FaceObjectResult(object):

    def __init__(self, return_code=-100, message="", age=None, top_left_coordinate=None, bottom_right_coordinate=None):
        self._return_code = return_code
        self._message = message
        self._age = age
        self._bounding_box = BoundingBox(top_left_coordinate, bottom_right_coordinate)

    @property
    def return_code(self) -> int:
        """
        Returns the return code for the image
        """
        return self._return_code

    @property
    def message(self) -> str:
        """
        Returns the message of the operation
        """
        return self._message

    @property
    def age(self) -> float:
        """
        Returns the predicted age of the image

        Age value might be in the float format as it is returned from DNN model
        """
        return self._age

    @property
    def bounding_box(self) -> BoundingBox:
        """Returns the bounding box for the images found

        Returns
        -------
        BoundingBox
            top_left_coordinate: Point

            bottom_right_coordinate: Point
        """
        return self._bounding_box

    @return_code.setter
    def return_code(self, value):
        self._return_code = value

    @message.setter
    def message(self, value):
        self._message = value

    @age.setter
    def age(self, value):
        self._age = value

    @bounding_box.setter
    def bounding_box(self, value):
        self._bounding_box = value

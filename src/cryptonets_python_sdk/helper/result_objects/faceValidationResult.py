from typing import List

from ..result_objects.faceObjectResult import FaceObjectResult


class FaceValidationResult:
    def __init__(self, error=-1, message=""):
        """Face validation result class for handling the detected faces
        """
        self._error = error
        self._message = message
        self._face_objects = []

    @property
    def error(self) -> int:
        """
        Returns the status of the operation
        """
        return self._error

    @property
    def message(self) -> str:
        """
        Returns the message of the operation
        """
        return self._message

    @property
    def face_objects(self) -> List[FaceObjectResult]:
        """
        Returns the list of Face Objects
        """
        return self._face_objects

    def append_face_objects(
        self,
        return_code=-100,
        message="",
        age=None,
        top_left_coordinate=None,
        bottom_right_coordinate=None,
    ):
        self._face_objects.append(
            FaceObjectResult(
                return_code=return_code,
                message=message,
                age=age,
                top_left_coordinate=top_left_coordinate,
                bottom_right_coordinate=bottom_right_coordinate,
            )
        )

    @message.setter
    def message(self, value):
        self._message = value

    @face_objects.setter
    def face_objects(self, value):
        self._face_objects = value

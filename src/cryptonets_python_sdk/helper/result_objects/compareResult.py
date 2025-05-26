class FaceCompareResult:
    # TODO once teh spec is clear, pickup proper names
    # for status and code like CALL_STATUS_SUCCESS ...,
    # ERROR_CODE_
    CALL_STATUS_SUCCESS = 0
    CALL_STATUS_ERROR = -1
    RESULT_SAME_FACE = 1
    RESULT_DIFFERENT_FACE = -1

    def __init__(
        self,
        result=RESULT_DIFFERENT_FACE,
        distance=None,
        second_validation_result=None,
        first_validation_result=None,
        status=CALL_STATUS_ERROR,
        message="",
    ):
        """Result handler for compare
        """
        self._status = status
        self._result = result
        self._message = message        
        self._distance = distance
        self._first_validation_result = first_validation_result
        self._second_validation_result = second_validation_result

    @property
    def status(self) -> int:
        """
        Returns the status of the operation

        0 - If the compare call was successful (regardless of the result)

        -1 - In case of error and the compare was not performed because of an error

        """
        return self._status

    @property
    def result(self) -> int:
        """
        Returns the result of the operation
        1  - if 2 images are same
        -1 - if 2 images are different
        """
        return self._result

    @property
    def message(self) -> str:
        """
        Returns the message of the operation
        """
        return self._message

    @property
    def distance(self) -> float:
        """
        Returns the comparaison distance
        
        """
        return self._distance

    @property
    def first_validation_result(self) -> int:
        """
        Returns the validation result of first image
        """
        return self._first_validation_result

    @property
    def second_validation_result(self) -> int:
        """
        Returns the validation result of second image
        """
        return self._second_validation_result

    @status.setter
    def status(self, value):
        self._status = value

    @result.setter
    def result(self, value):
        self._result = value

    @message.setter
    def message(self, value):
        self._message = value

    @distance.setter
    def distance(self, value):
        self._distance = value

    
    @first_validation_result.setter
    def first_validation_result(self, value):
        self._first_validation_result = value

    @second_validation_result.setter
    def second_validation_result(self, value):
        self._second_validation_result = value

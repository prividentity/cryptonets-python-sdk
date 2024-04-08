class FaceCompareResult:
    # TODO once teh spec is clear, pickup proper names
    # for status and code like CALL_STATUS_SUCCESS ...,
    # ERROR_CODE_
    CALL_STATUS_SUCCESS = 0
    CALL_STATUS_ERROR = -1

    def __init__(
        self,
        result=None,
        distance_min=None,
        distance_mean=None,
        distance_max=None,
        second_validation_result=None,
        first_validation_result=None,
        status=CALL_STATUS_ERROR,
        distance=None,
        message="",
    ):
        """Result handler for compare
        """
        self._status = status
        self._result = result
        self._message = message
        self.distance=distance
        self._distance_min = distance_min
        self._distance_mean = distance_mean
        self._distance_max = distance_max
        self._first_validation_result = first_validation_result
        self._second_validation_result = second_validation_result

    @property
    def status(self) -> int:
        """
        Returns the status of the operation

        0 - If successfully obtained result from server

        -1 - In case of error

        """
        return self._status

    @property
    def result(self) -> int:
        """
        Returns the result of the operation
        """
        return self._result

    @property
    def message(self) -> str:
        """
        Returns the message of the operation
        """
        return self._message

    @property
    def distance_min(self) -> float:
        """
        Returns the minimum distance

        Minimum distance refers to the thresholds used for comparing the images

        """
        return self._distance_min

    @property
    def distance_mean(self) -> float:
        """
        Returns the average distance

        Mean distance refers to the thresholds used for comparing the images

        """
        return self._distance_mean

    @property
    def distance_max(self) -> float:
        """
        Returns the maximum distance

        Maximum distance refers to the thresholds used for comparing the images

        """
        return self._distance_max

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

    @distance_min.setter
    def distance_min(self, value):
        self._distance_min = value

    @distance_mean.setter
    def distance_mean(self, value):
        self._distance_mean = value

    @distance_max.setter
    def distance_max(self, value):
        self._distance_max = value

    @first_validation_result.setter
    def first_validation_result(self, value):
        self._first_validation_result = value

    @second_validation_result.setter
    def second_validation_result(self, value):
        self._second_validation_result = value

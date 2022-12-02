class FaceIsValidDeprecatedResult:
    def __init__(self, result=None, age_factor=None, output_image_data=None, status=-1, message=""):
        self._status = status
        self._message = message
        self._result = result
        self._age_factor = age_factor
        self._output_image_data = output_image_data

    @property
    def status(self) -> int:
        """
        Returns the status of the operation

        0 - If successfully obtained result from server

        -1 - In case of error

        """
        return self._status

    @property
    def message(self) -> str:
        """
        Returns the message of the operation
        """
        return self._message

    @property
    def result(self) -> int:
        """
        Returns the result of the operation
        """
        return self._result

    @property
    def age_factor(self) -> float:
        """
        Returns the predicted age of the image

        Age value might be in the float format as it is returned from DNN model
        """
        return self._age_factor

    @property
    def output_image_data(self):
        """
        Returns the cropped image data from the image

        This is optional, configuration has to be implemented to extract data
        """
        return self._output_image_data

    @status.setter
    def status(self, value):
        self._status = value

    @message.setter
    def message(self, value):
        self._message = value

    @result.setter
    def result(self, value):
        self._result = value

    @age_factor.setter
    def age_factor(self, value):
        self._age_factor = value

    @output_image_data.setter
    def output_image_data(self, value):
        self._output_image_data = value

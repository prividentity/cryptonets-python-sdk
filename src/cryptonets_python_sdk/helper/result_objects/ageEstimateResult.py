class FaceAgeResult:
    def __init__(self, age=None, status=-1, message=""):
        self._status = status
        self._message = message
        self._age = age

    @property
    def status(self):
        """
        Returns the status of the operation

        0 - If successfully obtained result from server

        -1 - In case of error

        """
        return self._status

    @property
    def message(self):
        """
        Returns the message of the operation
        """
        return self._message

    @property
    def age(self):
        """
        Returns the predicted age of the image

        Age value might be in the float format as it is returned from DNN model
        """
        return self._age

    @status.setter
    def status(self, value):
        self._status = value

    @message.setter
    def message(self, value):
        self._message = value

    @age.setter
    def age(self, value):
        self._age = value

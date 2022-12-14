class FaceIsValidResult:
    def __init__(self,status=-1, message=""):
        self._status = status
        self._message = message

    @property
    def status(self):
        """
        Returns the status of the operation
        """
        return self._status

    @property
    def message(self):
        """
        Returns the message of the operation
        """
        return self._message

    @status.setter
    def status(self, value):
        self._status = value

    @message.setter
    def message(self, value):
        self._message = value

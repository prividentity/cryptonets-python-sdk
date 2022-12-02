class FaceDeleteResult:
    def __init__(self, status=-1, message=""):
        self._status = status
        self._message = message

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

    @message.setter
    def message(self, value):
        self._message = value

    @status.setter
    def status(self, value):
        self._status = value

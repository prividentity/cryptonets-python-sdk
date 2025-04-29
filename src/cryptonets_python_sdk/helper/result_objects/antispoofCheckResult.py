class AntispoofCheckResult:
    def __init__(self, status=None, message="", is_spoof=False):
        self._status = status
        self._message = message
        self._is_spoof = is_spoof

    @property
    def status(self) -> int:
        """
        Returns the status of the operation.
        """
        return self._status

    @property
    def message(self) -> str:
        """
        Returns a descriptive message associated with operation result.
        """
        return self._message

    @property
    def is_spoof(self) -> bool:
        """
        Returns a boolean indicating if the operation detected spoofing, False otherwise.
        """
        return self._is_spoof

    @status.setter
    def status(self, value):
        self._status = value

    @message.setter
    def message(self, value):
        self._message = value

    @is_spoof.setter
    def is_spoof(self, value):
        self._is_spoof = value

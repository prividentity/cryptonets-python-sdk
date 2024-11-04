class AntispoofCheckResult:
    def __init__(self, status=None, message="", is_antispoof=False):
        self._status = status
        self._message = message
        self._is_antispoof = is_antispoof

    @property
    def status(self) -> int:
        """
        Returns the status of the anti-spoofing operation.
        """
        return self._status

    @property
    def message(self) -> str:
        """
        Returns a descriptive message associated with the anti-spoofing operation result.
        """
        return self._message

    @property
    def is_antispoof(self) -> bool:
        """
        Returns a boolean indicating if the anti-spoofing operation detected spoofing.
        """
        return self._is_antispoof

    @status.setter
    def status(self, value):
        self._status = value

    @message.setter
    def message(self, value):
        self._message = value

    @is_antispoof.setter
    def is_antispoof(self, value):
        self._is_antispoof = value

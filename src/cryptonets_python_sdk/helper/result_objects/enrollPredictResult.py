class FaceEnrollPredictResult:
    def __init__(self, enroll_level=None, uuid=None, guid=None, token=None, status=-1, message=""):
        self._enroll_level = enroll_level
        self._uuid = uuid
        self._guid = guid
        self._token = token
        self._status = status
        self._message = message

    @property
    def enroll_level(self) -> int:
        """
        Returns the enroll_level of the user
        0 - one-factor authentication

        1 - two-factor authentication
        """
        return self._enroll_level

    @property
    def uuid(self) -> str:
        """
        Returns the UUID of the user

        Unique ID of length 20
        """
        return self._uuid

    @property
    def guid(self) -> str:
        """
        Returns the GUID of the user

        Unique ID of length 20
        """
        return self._guid

    @property
    def token(self) -> str:
        """
        Returns the token for verifying the operation

        Yet to be implemented for configuration
        """
        return self._token

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

    @enroll_level.setter
    def enroll_level(self, value):
        self._enroll_level = value

    @guid.setter
    def guid(self, value):
        self._guid = value

    @uuid.setter
    def uuid(self, value):
        self._uuid = value

    @status.setter
    def status(self, value):
        self._status = value

    @token.setter
    def token(self, value):
        self._token = value

    @message.setter
    def message(self, value):
        self._message = value

class FaceEnrollPredictResult:
    CALL_STATUS_SUCCESS = 0
    CALL_STATUS_ERROR = -1

    def __init__(
        self,
        enroll_level=None,
        puid=None,
        guid=None,
        token=None,
        code=None,
        score=None,
        status=CALL_STATUS_ERROR,
        message="",
        api_message="",
        api_status=None,
        enroll_performed=False
    ):
        self._enroll_level = enroll_level
        self._puid = puid
        self._guid = guid
        self._token = token
        self._status = status
        self._message = message
        self._code = code
        self._score = score
        self._api_message = api_message,
        self._api_status = api_status,
        self._enroll_performed = enroll_performed

    @property 
    def enroll_performed(self) -> bool:
        """
        Returns True if enroll was actually performed,
        False otherwise
        This property is only relevant for the enroll operation
        """
        return self._enroll_performed

    @property
    def api_message(self) -> str:
        """
        Returns the message received from the API of the operation
        """
        return self._api_message
    
    @property
    def api_status(self) -> str:
        """
        Returns the status received from the API of the operation
        0 - Success
        else - Failure
        """
        return self._api_status

    @property
    def enroll_level(self) -> int:
        """
        Returns the enroll_level of the user
        0 - one-factor authentication

        1 - two-factor authentication
        """
        return self._enroll_level

    @property
    def puid(self) -> str:
        """
        Returns the PUID of the user

        Unique ID of length 20
        """
        return self._puid

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
    @property
    def score(self) -> str:
        """
        Returns the message of the operation
        """
        return self._score
    @property
    def code(self) -> int:
        """
        Returns The field 'code' is a code or error value returned of the operation, this is needed t distinguish
        between what data is returned by a successful enroll or predict calls from the success of the call itself.
        A call is successful if it returned an intelligible JSON.
        TODO: 1) the field 'code '  to be split in 2 fields after the fix the spec in c/c++ code
        TODO: 2) pickup a proper name like to express the nature of these codes like error_code, validation_code etc.
        """
        return self._code

    @enroll_level.setter
    def enroll_level(self, value):
        self._enroll_level = value

    @guid.setter
    def guid(self, value):
        self._guid = value

    @puid.setter
    def puid(self, value):
        self._puid = value

    @status.setter
    def status(self, value):
        self._status = value

    @token.setter
    def token(self, value):
        self._token = value

    @message.setter
    def message(self, value):
        self._message = value

    @code.setter
    def code(self, value):
        self._code = value

    @api_message.setter
    def api_message(self, value):
        self._api_message = value

    @api_status.setter
    def api_status(self, value):
        self._api_status = value
    
    @enroll_performed.setter
    def enroll_performed(self, value):
        self._enroll_performed = value
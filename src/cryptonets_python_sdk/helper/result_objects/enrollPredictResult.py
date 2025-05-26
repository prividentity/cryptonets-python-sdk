from typing import Union, List

class FaceEnrollPredictResult:
    CALL_STATUS_SUCCESS = 0
    CALL_STATUS_ERROR = -1

    def __init__(
        self,
        enroll_level=None,
        puid=None,
        guid=None,
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
        self._status = status
        self._message = message
        self._score = score
        self._api_message = api_message
        self._api_status = api_status
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
        Returns the message received from the API of the operation.
        If the user is enrolled, this message will be "User Already Enrolled"
        """
        return self._api_message
    
    @property
    def api_status(self) -> int:
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
        Returns the score obtained from server
        """
        return self._score        
    
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

    @message.setter
    def message(self, value):
        self._message = value
    
    @api_message.setter
    def api_message(self, value):
        self._api_message = value

    @api_status.setter
    def api_status(self, value):
        self._api_status = value
    
    @enroll_performed.setter
    def enroll_performed(self, value):
        self._enroll_performed = value

    @staticmethod
    def print(result: Union['FaceEnrollPredictResult', List['FaceEnrollPredictResult']]) -> None:
        """
        Print the result of the enroll or predict operation
        
        Args:
            result (Union[FaceEnrollPredictResult, List[FaceEnrollPredictResult]]): The result of the operation
        """
        if isinstance(result, list):
            print("FaceEnrollPredictResult  List:")
            for item in result:
                print(item)
        elif isinstance(result, FaceEnrollPredictResult):
            print("FaceEnrollPredictResult  Item:")
            print(f"Status: {result.status}")
            print(f"Message: {result.message}")
            print(f"Enroll Level: {result.enroll_level}")
            print(f"PUID: {result.puid}")
            print(f"GUID: {result.guid}")            
            print(f"Score: {item.score}")
            print(f"API Status: {result.api_status}")
            print(f"API Message: {result.api_message}")
            print(f"Enroll Performed: {result.enroll_performed}")
        else:
            print("Argument is not a `FaceEnrollPredictResult` type.")
    
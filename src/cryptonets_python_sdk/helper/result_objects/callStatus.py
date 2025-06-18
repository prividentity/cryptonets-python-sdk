from dataclasses import dataclass
from typing import Optional, Dict, Any
from enum import Enum, EnumMeta


class ApiReturnStatusMeta(EnumMeta):
    def __contains__(cls, item):
        return item in [v.value for v in cls.__members__.values()]


class ApiReturnStatus(Enum, metaclass=ApiReturnStatusMeta):
    """
    Enumeration of possible API return statuses.

    Attributes:
        API_NO_ERROR (int): Status for success.
        API_INVALID_SESSION_HANDLER (int): Session handler is invalid, for calls that need a valid session.
        API_INVALID_CONFIGURATION (int): For calls which provide configuration data.
        API_INVALID_ARGUMENT (int): Logical error due to an unexpected value for a certain argument of the API call.
        API_NETWORK_ERROR (int): Networking problem preventing the operation from being performed.
        API_GENERIC_ERROR (int): Generic runtime error; caller may find hints in the attached return message.
        API_UNHANDLED_EXCEPTION (int): Unhandled exception occurred, interrupting the operation (no recovery actions performed).
        API_MAL_FORMED_AP_RESPONSE (int): Malformed API response data received.
        API_AUTHORIZATION_ERROR (int): Authorization error due to wrong API key, token, public key, etc., or a similar error.
    """
    # Status for success.
    API_NO_ERROR = 0
    # Session handler is invalid, for calls that needs a valid session.
    API_INVALID_SESSION_HANDLER = 2
    # For calls which provides a configuration data.
    API_INVALID_CONFIGURATION = 4    
    # A generic error to specify a logical error about an unexpected value for a certain argument
    # of the API call.
    API_INVALID_ARGUMENT = 5    
    # A networking problem preventing the operation to be performed.
    API_NETWORK_ERROR = 6 
    # A generic runtime error, the caller may find hints on the attached ApiReturn::return_message.
    API_GENERIC_ERROR = 7
    # An unhandled exception that occurred interrupting the operation.(no recovery actions were performed). 
    API_UNHANDLED_EXCEPTION = 8
    # We received a malformed API response data. 
    API_MAL_FORMED_AP_RESPONSE = 9
    # Authorization error due to wrong API key or wrong token, public key etc.. or a similar error.
    API_AUTHORIZATION_ERROR = 10



@dataclass
class CallStatus:
    """Data class representing the call status response from the native API call."""
    return_status: int
    operation_tag: str
    return_message: str
    mf_token: str
    operation_id: int
    operation_type_id: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CallStatus':
        """
        Deserialize a dictionary into a CallStatus object.
        
        Args:
            data: Dictionary containing call status information
            
        Returns:
            CallStatus object
        """
        return cls(
            return_status=data.get('return_status', ApiReturnStatus.API_GENERIC_ERROR.value),
            operation_tag=data.get('operation_tag', ''),
            return_message=data.get('return_message', ''),
            mf_token=data.get('mf_token', ''),
            operation_id=data.get('operation_id', 0),
            operation_type_id=data.get('operation_type_id', 0)
        )

    def is_success(self) -> bool:
        """Check if the call was successful based on return status."""
        return self.return_status == ApiReturnStatus.API_NO_ERROR.value
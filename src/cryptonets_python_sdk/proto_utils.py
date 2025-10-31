import cryptonets_python_sdk.generated.proto_python.messages 
import json

class proto_utils:
    @staticmethod
    def json_to_proto(json_data: dict) -> ApiResult:
        """
        Convert a JSON object to a proto message
        :param json_data: JSON object to convert
        :return: proto message
        """
        message = ApiResult()
        message.parse_from_json(json.dumps(json_data))
        return message
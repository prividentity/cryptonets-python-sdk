
import platform

from ..settings.loggingLevel import LoggingLevel
from ..settings.supportedPlatforms import SupportedPlatforms
import sys

class ModuleSettings:
    def __init__(self, api_key=None, server_url=None, local_storage_path="privateid",
                 logging_level=LoggingLevel.off.value):

        try:
            if not api_key or not server_url or not local_storage_path or logging_level is None:
                raise ValueError("Wrong parameters while initializing the SDK")
            if platform.system() not in SupportedPlatforms.supportedOS.value:
                raise OSError("Invalid OS")

            self._api_key = bytes(api_key, 'utf-8')
            self._local_storage_path = bytes(local_storage_path, 'utf-8')
            self._logging_level = logging_level
            if server_url[-1] == "/":
                server_url=server_url[:-1]
            self._server_url = bytes(server_url, 'utf-8')
        except ValueError as exp:
            print("Error", exp)
            sys.exit(1)
        except OSError as exp:
            print("Error", exp)
            sys.exit(1)
    @property
    def api_key(self):
        return self._api_key

    @property
    def server_url(self):
        return self._server_url

    @property
    def local_storage_path(self):
        return self._local_storage_path

    @property
    def logging_level(self):
        return self._logging_level

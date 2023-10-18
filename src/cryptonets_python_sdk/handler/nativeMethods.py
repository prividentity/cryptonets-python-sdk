import json
import pathlib
import sys
import platform
from typing import Any
import ctypes
from ctypes import POINTER, byref, c_void_p, c_bool, c_char_p, c_int, c_uint8
import numpy as np
from ..settings.cacheType import CacheType
from ..settings.configuration import ConfigObject
from ..settings.loggingLevel import LoggingLevel

class NativeMethods:

    def __init__(self,logging_level: LoggingLevel,
                 config_object: ConfigObject = None):
        try:
            self._config_object = config_object
            self._logging_level = logging_level
            self._face_setup()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

    def _face_setup(self):
        lib_path = str(pathlib.Path(__file__).parent.joinpath(f"lib/lib_fhe.{self._get_lib_extension()}").resolve())
        
        if platform.system() == "Windows":
            ssl_lib_path = str(pathlib.Path(__file__).parent.joinpath("lib/libssl-1_1-x64.dll").resolve())
            crypto_lib_path = str(pathlib.Path(__file__).parent.joinpath("lib/libcrypto-1_1-x64.dll").resolve())
            ctypes.CDLL(crypto_lib_path, mode=1)
            ctypes.CDLL(ssl_lib_path, mode=1)

        self._spl_so_face = ctypes.CDLL(lib_path)
        
        self._initialize_session()
        self._configure_library()

    def _initialize_session(self):
        self._spl_so_face.privid_initialize_session.argtypes = [
            c_int, POINTER(c_void_p)]
        self._spl_so_face.privid_initialize_session.restype = c_bool
        self._spl_so_face.handle = c_void_p()

        init_success = self._spl_so_face.privid_initialize_session(
            self._logging_level.value,
            byref(self._spl_so_face.handle))

        if not init_success:
            raise Exception("Initialization failed. Check API_KEY or Server URL.")

    def _configure_library(self):
        self._spl_so_face.privid_set_configuration.argtypes = [c_void_p, c_char_p, c_int]
        self._spl_so_face.privid_set_configuration.restype = c_bool

        if self._config_object and self._config_object.get_config_param():
            config_dict = json.loads(self._config_object.get_config_param())
            config_dict["cache_type"] = self._cache_type.value
            config_dict["local_storage_path"] = self._local_storage_path
            config_data = json.dumps(config_dict)
            c_config_data = c_char_p(bytes(config_data, 'utf-8'))
            c_config_len = c_int(len(config_data))
            self._spl_so_face.privid_set_configuration(self._spl_so_face.handle, c_config_data, c_config_len)

        self._spl_so_face.privid_free_char_buffer.argtypes = [c_char_p]
        self._spl_so_face.privid_free_char_buffer.restype = c_void_p
        
        self._spl_so_face.privid_estimate_age_be.argtypes = [
            c_void_p, POINTER(c_uint8), c_int, c_int, c_char_p, c_int, POINTER(c_char_p), POINTER(c_int)]
        self._spl_so_face.privid_estimate_age_be.restype = c_bool

        
    def _get_lib_extension(self):
        sys_platform = platform.system()
        if sys_platform == "Linux":
            return "so"
        elif sys_platform == "Windows":
            return "dll"
        elif sys_platform == "Darwin":
            return "dylib"
        else:
            raise ValueError(f"Unsupported system platform: {sys_platform}")

    def update_config(self, config_object):
        if self._config_object and self._config_object.get_config_param():
            config_data = self._config_object.get_config_param()
            self._update_native_configuration(config_data)

    def _update_native_configuration(self, config_data: str):
        c_config_param = c_char_p(bytes(config_data, 'utf-8'))
        c_config_param_len = c_int(len(config_data))
        self._spl_so_face.privid_set_configuration(self._spl_so_face.handle, c_config_param, c_config_param_len)

    def estimate_age(self, image_data: np.array, config_object: ConfigObject = None) -> Any:
        try:
            img_width, img_height = image_data.shape[1], image_data.shape[0]
            img_data_ptr = image_data.flatten().ctypes.data_as(POINTER(c_uint8))

            c_result = c_char_p()
            c_result_len = c_int()

            config_data = config_object.get_config_param() if config_object else ""
            c_config_param = c_char_p(bytes(config_data, 'utf-8'))
            c_config_param_len = c_int(len(config_data))

            self._spl_so_face.privid_estimate_age_be(self._spl_so_face.handle,
                                                  img_data_ptr,
                                                  c_int(img_width),
                                                  c_int(img_height),
                                                  c_config_param,
                                                  c_config_param_len,
                                                  byref(c_result),
                                                  byref(c_result_len))

            if not c_result.value or not c_result_len.value:
                raise Exception("Something went wrong. Couldn't process the image for estimate_age API.")

            output_json = c_result.value[:c_result_len.value].decode()
            self._spl_so_face.privid_free_char_buffer(c_result)
            return json.loads(output_json)
        except Exception as e:
            print(e)
            return False

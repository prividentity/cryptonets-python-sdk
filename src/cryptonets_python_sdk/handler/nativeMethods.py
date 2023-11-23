import ctypes
import json
import pathlib
import sys
from ctypes import *
from typing import Any
import numpy as np
from PIL import Image
import platform
from ..settings.cacheType import CacheType
from ..settings.configuration import ConfigObject
from ..settings.loggingLevel import LoggingLevel
import boto3
import botocore
import tqdm
class NativeMethods(object):
    def __init__(
        self,
        api_key: str,
        server_url: str,
        local_storage_path: str,
        logging_level: LoggingLevel,
        tf_num_thread: int,
        cache_type: CacheType,
        config_object: ConfigObject = None,
    ):
        try:
            self._config_object = config_object
            self._local_lib_path = pathlib.Path(__file__).parent.joinpath("lib")
            self._local_lib_path.mkdir(parents=True, exist_ok=True)
            self._check_and_download_files()

            if platform.system() == "Linux":
                self._load_linux_libraries()
            elif platform.system() == "Windows":
                self._load_windows_libraries()
            elif platform.system() == "Darwin":
                self._load_macos_libraries()
            self._initialize_properties(tf_num_thread, api_key, server_url, local_storage_path, logging_level, cache_type)
            self._face_setup()
        except Exception as e:
            print("Error ", e)
            sys.exit(1)

    def _check_and_download_files(self):
        required_files = [
            "lib_fhe.so",
            "libcrypto-1_1-x64.dll",
            "libprivid_fhe.dylib",
            "libssl-1_1-x64.dll",
            "privid_fhe.dll"
        ]
       # Create an unauthenticated session
        session = boto3.Session()
        s3 = session.client('s3', config=botocore.config.Config(signature_version=botocore.UNSIGNED))
        bucket_name = "cryptonets-python-sdk"

        for file_name in required_files:
            file_path = self._local_lib_path.joinpath(file_name)
            if not file_path.exists():
                print(f"Downloading {file_name}...")
                self._download_from_s3(s3, bucket_name, file_name, file_path)

    def _download_from_s3(self, s3_client, bucket, file_name, local_path):
        with open(local_path, 'wb') as f:
            response = s3_client.get_object(Bucket=bucket, Key=file_name)
            file_size = response['ContentLength']

            with tqdm.tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name) as bar:
                for chunk in response['Body'].iter_chunks(chunk_size=1024):
                    f.write(chunk)
                    bar.update(len(chunk))

    def _load_linux_libraries(self):
        self._library_path = str(self._local_lib_path.joinpath("lib_fhe.so").resolve())
        self._spl_so_face = ctypes.CDLL(self._library_path)

    def _load_windows_libraries(self):
        self._library_path = str(self._local_lib_path.joinpath("privid_fhe.dll").resolve())
        self._library_path_2 = str(self._local_lib_path.joinpath("libssl-1_1-x64.dll").resolve())
        self._library_path_3 = str(self._local_lib_path.joinpath("libcrypto-1_1-x64.dll").resolve())
        ctypes.CDLL(self._library_path_3, mode=1)
        ctypes.CDLL(self._library_path_2, mode=1)
        self._spl_so_face = ctypes.CDLL(self._library_path)

    def _load_macos_libraries(self):
        self._library_path = str(self._local_lib_path.joinpath("libprivid_fhe.dylib").resolve())
        self._spl_so_face = ctypes.CDLL(self._library_path)

    def _initialize_properties(self, tf_num_thread, api_key, server_url, local_storage_path, logging_level, cache_type):
        self._embedding_length = 128
        self._num_embeddings = 80
        self._aug_size = 224 * 224 * 4 * self._num_embeddings
        self._tf_num_thread = tf_num_thread
        self._api_key = bytes(api_key, "utf-8")
        self._server_url = bytes(server_url, "utf-8")
        self._logging_level = logging_level
        self._local_storage_path = local_storage_path
        self._cache_type = cache_type


# class NativeMethods(object):
#     def __init__(
#         self,
#         api_key: str,
#         server_url: str,
#         local_storage_path: str,
#         logging_level: LoggingLevel,
#         tf_num_thread: int,
#         cache_type: CacheType,
#         config_object: ConfigObject = None,
#     ):
#         try:
#             self._config_object = config_object
#             if platform.system() == "Linux":
#                 self._library_path = str(
#                     pathlib.Path(__file__)
#                     .parent.joinpath("lib/lib_fhe.so")
#                     .resolve()
#                 )
#                 self._spl_so_face = ctypes.CDLL(self._library_path)
#             elif platform.system() == "Windows":
#                 self._library_path = str(
#                     pathlib.Path(__file__)
#                     .parent.joinpath("lib/privid_fhe.dll")
#                     .resolve()
#                 )
#                 self._library_path_2 = str(
#                     pathlib.Path(__file__)
#                     .parent.joinpath("lib/libssl-1_1-x64.dll")
#                     .resolve()
#                 )
#                 self._library_path_3 = str(
#                     pathlib.Path(__file__)
#                     .parent.joinpath("lib/libcrypto-1_1-x64.dll")
#                     .resolve()
#                 )
#                 ctypes.CDLL(self._library_path_3, mode=1)
#                 ctypes.CDLL(self._library_path_2, mode=1)
#                 self._spl_so_face = ctypes.CDLL(self._library_path)
#             elif platform.system() == "Darwin":
#                 self._library_path = str(
#                     pathlib.Path(__file__)
#                     .parent.joinpath("lib/libprivid_fhe.dylib")
#                     .resolve()
#                 )
#                 self._spl_so_face = ctypes.CDLL(self._library_path)

#             self._embedding_length = 128
#             self._num_embeddings = 80
#             self._aug_size = 224 * 224 * 4 * self._num_embeddings
#             self._tf_num_thread = tf_num_thread
#             self._api_key = bytes(api_key, "utf-8")
#             self._server_url = bytes(server_url, "utf-8")
#             self._logging_level = logging_level
#             self._local_storage_path = local_storage_path
#             self._cache_type = cache_type
#             self._face_setup()
#         except Exception as e:
#             print("Error ", e)
#             sys.exit(1)

    def update_config(self, config_object):
        self._config_object = config_object
        if self._config_object and self._config_object.get_config_param():
            c_config_param = c_char_p(
                bytes(self._config_object.get_config_param(), "utf-8")
            )
            c_config_param_len = c_int(len(self._config_object.get_config_param()))
            self._spl_so_face.privid_set_configuration(
                self._spl_so_face.handle, c_config_param, c_config_param_len
            )

    def _face_setup(self):

        # set the API ctypes wrapped methods and perform session initialization steps

        ##############################################################################################
        # (ok) PRIVID_API_ATTRIB bool privid_initialize_session(
        #         const char* api_key, const unsigned int key_api_length,
        #         const char* base_url, const unsigned int base_url_length,
        #         const int debug_level,void** session_ptr_out);
        ##############################################################################################

        self._spl_so_face.privid_initialize_session.argtypes = [
            c_char_p,  # const char* api_key
            c_int,  # const unsigned int key_api_length
            c_char_p,  # const char* base_url
            c_int,  # const unsigned int base_url_length
            c_int,
            c_int,  # const int debug_level
            POINTER(c_void_p),
        ]  # void** session_ptr_out
        self._spl_so_face.privid_initialize_session.restype = c_bool
        self._spl_so_face.handle = c_void_p()  # TODO rename to session
        # create a session

        return_type = self._spl_so_face.privid_initialize_session(
            c_char_p(self._api_key),
            c_int32(len(self._api_key)),
            c_char_p(self._server_url),
            c_int32(len(self._server_url)),
            c_int32(5000),
            self._logging_level.value,
            byref(self._spl_so_face.handle),
        )
        if not return_type:
            raise Exception("Wrong API_KEY or Server URL.")
        ##############################################################################################

        ##############################################################################################
        # (ok) PRIVID_API_ATTRIB bool privid_set_configuration(void *session_ptr, const char *user_config,
        # const int user_config_length);
        ##############################################################################################
        self._spl_so_face.privid_set_configuration.argtypes = [
            c_void_p,  # void *session_ptr
            c_char_p,  # const char *user_config
            c_int,
        ]  # const int user_config_length
        self._spl_so_face.privid_set_configuration.restype = c_bool
        # Configure parameters
        if self._config_object is None:
            config_dict={}
            config_dict["skip_antispoof"] = True
            config_dict = json.dumps(config_dict)
            c_config_param = c_char_p(bytes(config_dict, "utf-8"))
            c_config_param_len = c_int(len(config_dict))
            self._spl_so_face.privid_set_configuration(
                self._spl_so_face.handle, c_config_param, c_config_param_len
            )    
        elif self._config_object and self._config_object.get_config_param():
            config_dict = json.loads(self._config_object.get_config_param())
            config_dict["cache_type"] = self._cache_type.value
            config_dict["local_storage_path"] = self._local_storage_path

            config_dict["skip_antispoof"] = True
            config_dict = json.dumps(config_dict)
            c_config_param = c_char_p(bytes(config_dict, "utf-8"))
            c_config_param_len = c_int(len(config_dict))
            self._spl_so_face.privid_set_configuration(
                self._spl_so_face.handle, c_config_param, c_config_param_len
            )
        ###############################################################################################

        ##############################################################################################
        # (ok) PRIVID_API_ATTRIB int privid_enroll_onefa(
        #         void *session_ptr, const char *user_config, const int user_config_length,
        #         const uint8_t *input_images, const int image_count, const int image_size,
        #         const int image_width, const int image_height,
        #         uint8_t** best_input_out, int *best_input_length,
        #         char **result_out, int *result_out_length);
        ##############################################################################################
        self._spl_so_face.privid_enroll_onefa.argtypes = [
            c_void_p,  # void *session_ptr
            c_char_p,  # const char *user_config
            c_int,  # const int user_config_length
            POINTER(c_uint8),  # const uint8_t *input_images
            c_int,  # const int image_count
            c_int,  # const int image_size
            c_int,  # const int image_width,
            c_int,  # const int image_height
            POINTER(c_uint8),  # uint8_t** best_input_out
            POINTER(c_int),  # int *best_input_length
            POINTER(c_char_p),  # char **result_out
            POINTER(c_int),
        ]  # int *result_out_length
        self._spl_so_face.privid_enroll_onefa.restype = c_int
        ##############################################################################################

        ##############################################################################################
        # (ok) PRIVID_API_ATTRIB int privid_face_predict_onefa(
        #           void *session_ptr, const char *user_config, const int user_config_length,
        #           const uint8_t *input_images, const int image_count, const int image_size,
        #           const int image_width, const int image_height,
        #           char **result_out, int *result_out_length);
        ##############################################################################################
        self._spl_so_face.privid_face_predict_onefa.argtypes = [
            c_void_p,  # void *session_ptr
            c_char_p,  # const char *user_config
            c_int,  # const int user_config_length
            POINTER(c_uint8),  # const uint8_t *input_images,
            c_int,  # const int image_count,
            c_int,  # const int image_size,
            c_int,  # const int image_width,
            c_int,  # const int image_height,
            POINTER(c_char_p),  # char **result_out,
            POINTER(c_int),
        ]  # int *result_out_length
        self._spl_so_face.privid_face_predict_onefa.restype = c_int
        ##############################################################################################

        ##############################################################################################
        # (ok) PRIVID_API_ATTRIB int privid_user_delete(
        #         void *session_ptr, const char *user_conf, const int conf_len,
        #         const char *puid, const int puid_length,
        #         char **operation_result_out, int *operation_result_out_len);
        ##############################################################################################
        self._spl_so_face.privid_user_delete.argtypes = [
            c_void_p,  # void *session_ptr
            POINTER(c_char),  # const char *user_conf
            c_int,  # const int conf_len
            POINTER(c_char),  # const char *puid
            c_int,  # const int puid_length
            POINTER(c_char_p),  # char **operation_result_out
            POINTER(c_int),
        ]  # int *operation_result_out_len
        self._spl_so_face.privid_user_delete.restype = c_int
        ##############################################################################################

        ##############################################################################################
        # (ok) PRIVID_API void privid_free_char_buffer(char **buffer);
        ##############################################################################################
        self._spl_so_face.privid_free_char_buffer.argtypes = [c_char_p]  # char **buffer
        ##############################################################################################

        ##############################################################################################
        # (ok) PRIVID_API_ATTRIB bool privid_face_compare_files(
        #         void* session_ptr, float fudge_factor,
        #         const char* user_config, int user_config_length,
        #         const uint8_t* p_buffer_files_A, int im_size_A, int im_width_A, int im_height_A,
        #         const uint8_t* p_buffer_files_B, int im_size_B, int im_width_B, int im_height_B,
        #         char** result_out, int* result_out_length);
        ##############################################################################################
        self._spl_so_face.privid_face_compare_files.argtypes = [
            c_void_p,  # void* session_ptr
            c_float,  # float fudge_factor
            c_char_p,  # const char* user_config
            c_int,  # int user_config_length
            POINTER(c_uint8),  # const uint8_t* p_buffer_files_A,
            c_int,  # int im_size_A
            c_int,  # int im_width_A
            c_int,  # int im_height_A
            POINTER(c_uint8),  # const uint8_t* p_buffer_files_B,
            c_int,  # int im_size_B,
            c_int,  # int im_width_B,
            c_int,  # int im_height_B
            POINTER(c_char_p),  # char** result_out
            POINTER(c_int),
        ]  # int* result_out_length
        self._spl_so_face.privid_face_compare_files.restype = c_int
        ##############################################################################################

        ##############################################################################################
        # (ok) PRIVID_API_ATTRIB bool privid_validate(
        #         void *session_ptr, const uint8_t* image_bytes, const int image_width,
        #         const int image_height,const char *user_config, const int user_config_length,
        #         char **result_out, int *result_out_length);
        ##############################################################################################
        self._spl_so_face.privid_validate.argtypes = [
            c_void_p,  # void *session_ptr
            POINTER(c_uint8),  # const uint8_t* image_bytes
            c_int,  # const int image_width
            c_int,  # const int image_height
            c_char_p,  # const char *user_config
            c_int,  # const int user_config_length
            POINTER(c_char_p),  # char **result_out
            POINTER(c_int),
        ]  # int *result_out_length
        self._spl_so_face.privid_validate.restype = c_bool
        ##############################################################################################

        ##############################################################################################
        # (ok) PRIVID_API_ATTRIB bool privid_estimate_age(
        #         void *session_ptr, const uint8_t* image_bytes, const int image_width,
        #         const int image_height,const char *user_config, const int user_config_length,
        #         char **result_out, int *result_out_length);
        ##############################################################################################
        self._spl_so_face.privid_estimate_age.argtypes = [
            c_void_p,  # void *session_ptr
            POINTER(c_uint8),  # const uint8_t* image_bytes
            c_int,  # const int image_width
            c_int,  # const int image_height,
            c_char_p,  # const char *user_config,
            c_int,  # const int user_config_length
            POINTER(c_char_p),  # char **result_out
            POINTER(c_int),
        ]  # int *result_out_length
        self._spl_so_face.privid_estimate_age.restype = c_bool

        ##############################################################################################
        # (ok) PRIVID_API_ATTRIB bool privid_face_iso(
        #         void *session_ptr, const uint8_t *image_bytes, const int image_width, const int image_height,
        #         const char *user_config, const int user_config_length, char **result_out, int *result_out_length,
        #         uint8_t** output_iso_image_bytes, int* output_iso_image_bytes_length);
        ##############################################################################################
        self._spl_so_face.privid_face_iso.argtypes = [
            c_void_p,  # void *session_ptr
            POINTER(c_uint8),  # const uint8_t *image_bytes
            c_int,  # const int image_width
            c_int,  # const int image_height
            c_char_p,  # const char *user_config
            c_int,  # const int user_config_length
            POINTER(c_char_p),  # char **result_out
            POINTER(c_int),  # int *result_out_length
            POINTER(POINTER(c_ubyte)),  # uint8_t** output_iso_image_bytes
            POINTER(c_int),
        ]  # int* output_iso_image_bytes_length
        self._spl_so_face.privid_face_iso.restype = c_bool  # fixed a bug here

        ##############################################################################################
        # (ok) PRIVID_API_ATTRIB bool privid_set_billing_record_threshold(
        #         void *session_ptr, const char *billing_config,
        #         const int billing_config_length);
        ##############################################################################################
        self._spl_so_face.privid_set_billing_record_threshold.argtypes = [
            c_void_p,  # void *session_ptr
            c_char_p,  # const char *billing_config
            c_int,
        ]  # const int billing_config_length
        self._spl_so_face.privid_set_billing_record_threshold.restype = c_bool
        ##############################################################################################

        ##############################################################################################
        #   D_API_ATTRIB bool privid_anti_spoofing(
        #   void* session_ptr, const uint8_t* image_bytes, const int image_width,
        #   const int image_height, const char* user_config, const int user_config_length,
        #   char** result_out, int* result_out_length);
        ##############################################################################################
        self._spl_so_face.privid_anti_spoofing.argtypes = [
            c_void_p,  # void *session_ptr
            POINTER(c_uint8),  # const uint8_t* image_bytes
            c_int,  # const int image_width
            c_int,  # const int image_height,
            c_char_p,  # const char *user_config,
            c_int,  # const int user_config_length
            POINTER(c_char_p),  # char **result_out
            POINTER(c_int),
        ]  # int *result_out_length
        self._spl_so_face.privid_anti_spoofing.restype = c_bool
        ##############################################################################################

        if self._config_object and self._config_object.get_config_billing_param():
            c_config_param = c_char_p(
                bytes(self._config_object.get_config_billing_param(), "utf-8")
            )
            c_config_param_len = c_int(
                len(self._config_object.get_config_billing_param())
            )
            self._spl_so_face.privid_set_billing_record_threshold(
                self._spl_so_face.handle, c_config_param, c_config_param_len
            )

    def is_valid_without_age(
        self, image_data: np.array, config_object: ConfigObject = None
    ) -> Any:
        try:
            img = image_data
            im_width = img.shape[1]
            im_height = img.shape[0]

            p_buffer_images_in = img.flatten()
            c_p_buffer_images_in = p_buffer_images_in.ctypes.data_as(POINTER(c_uint8))

            c_result = c_char_p()
            c_result_len = c_int()
            if config_object and config_object.get_config_param():
                c_config_param = c_char_p(
                    bytes(config_object.get_config_param(), "utf-8")
                )
                c_config_param_len = c_int(len(config_object.get_config_param()))
            else:
                c_config_param = c_char_p(bytes("", "utf-8"))
                c_config_param_len = c_int(0)
            self._spl_so_face.privid_validate(
                self._spl_so_face.handle,
                c_p_buffer_images_in,
                c_int(im_width),
                c_int(im_height),
                c_config_param,
                c_config_param_len,
                byref(c_result),
                byref(c_result_len),
            )

            if not c_result.value or not c_result_len.value:
                raise Exception(
                    "Something went wrong. Couldn't process the image for is_valid API. "
                )
            output_json = c_result.value[: c_result_len.value].decode()
            self._spl_so_face.privid_free_char_buffer(c_result)

            output = json.loads(output_json)
            return output
        except Exception as e:
            print(e)
            return False

    def estimate_age(
        self, image_data: np.array, config_object: ConfigObject = None
    ) -> Any:
        try:
            img = image_data
            im_width = img.shape[1]
            im_height = img.shape[0]

            p_buffer_images_in = img.flatten()
            c_p_buffer_images_in = p_buffer_images_in.ctypes.data_as(POINTER(c_uint8))

            c_result = c_char_p()
            c_result_len = c_int()
            if config_object and config_object.get_config_param():
                c_config_param = c_char_p(
                    bytes(config_object.get_config_param(), "utf-8")
                )
                c_config_param_len = c_int(len(config_object.get_config_param()))
            else:
                c_config_param = c_char_p(bytes("", "utf-8"))
                c_config_param_len = c_int(0)
            self._spl_so_face.privid_estimate_age(
                self._spl_so_face.handle,
                c_p_buffer_images_in,
                c_int(im_width),
                c_int(im_height),
                c_config_param,
                c_config_param_len,
                byref(c_result),
                byref(c_result_len),
            )

            if not c_result.value or not c_result_len.value:
                raise Exception(
                    "Something went wrong. Couldn't process the image for estimate_age API. "
                )
            output_json = c_result.value[: c_result_len.value].decode()
            self._spl_so_face.privid_free_char_buffer(c_result)

            output = json.loads(output_json)
            return output
        except Exception as e:
            print(e)
            return False

    def get_iso_face(
        self, image_data: np.array, config_object: ConfigObject = None
    ) -> Any:
        try:
            img = image_data
            im_width = img.shape[1]
            im_height = img.shape[0]

            p_buffer_images_in = img.flatten()
            c_p_buffer_images_in = p_buffer_images_in.ctypes.data_as(POINTER(c_uint8))

            c_result = c_char_p()
            c_result_len = c_int()
            c_iso_image_len = c_int()

            c_iso_image = POINTER(c_ubyte)()

            if config_object and config_object.get_config_param():
                c_config_param = c_char_p(
                    bytes(config_object.get_config_param(), "utf-8")
                )
                c_config_param_len = c_int(len(config_object.get_config_param()))
            else:
                c_config_param = c_char_p(bytes("", "utf-8"))
                c_config_param_len = c_int(0)

            self._spl_so_face.privid_face_iso(
                self._spl_so_face.handle,
                c_p_buffer_images_in,
                c_int(im_width),
                c_int(im_height),
                c_config_param,
                c_config_param_len,
                byref(c_result),
                byref(c_result_len),
                byref(c_iso_image),
                byref(c_iso_image_len),
            )

            if not c_result.value or not c_result_len.value:
                raise Exception(
                    "Something went wrong. Couldn't process the image for get_iso_face API. "
                )
            output_json = c_result.value[: c_result_len.value].decode()
            output_json = json.loads(output_json)
            self._spl_so_face.privid_free_char_buffer(c_result)
            if (
                c_iso_image_len.value
                and "iso_image_width" in output_json
                and "iso_image_height" in output_json
            ):
                output_json["image"] = Image.fromarray(
                    np.uint8(
                        np.reshape(
                            c_iso_image[: c_iso_image_len.value],
                            (
                                output_json.get("iso_image_height", 0),
                                output_json.get("iso_image_width", 0),
                                output_json.get("iso_image_channels", 0),
                            ),
                        )
                    )
                ).convert(
                    "RGBA" if output_json.get("iso_image_channels", 0) == 4 else "RGB"
                )
            else:
                # Empty Image
                output_json["image"] = Image.new("RGB", (800, 1280), (255, 255, 255))
            return output_json
        except Exception as e:
            print(e)
            return False

    def delete(self, puid: str) -> Any:
        puid = bytes(puid, "utf-8")
        p_buffer_result = c_char_p()
        p_buffer_result_length = c_int()
        c_config_param = c_char_p(bytes("", "utf-8"))
        c_config_param_len = c_int(0)
        self._spl_so_face.privid_user_delete(
            self._spl_so_face.handle,
            c_config_param,
            c_config_param_len,
            c_char_p(puid),
            c_int(len(puid)),
            byref(p_buffer_result),
            byref(p_buffer_result_length),
        )

        len_ = p_buffer_result_length.value
        if len_:
            output_json_str = p_buffer_result.value[:len_].decode()
        else: 
            return False
        self._spl_so_face.privid_free_char_buffer(p_buffer_result)
        if output_json_str is not None and len(output_json_str) > 0:
            output = json.loads(output_json_str)
            return output
        else:
            return False

    def compare_files(
        self,
        left_image: np.array,
        right_image: np.array,
        config_object: ConfigObject = None,
    ) -> Any:
        fudge_factor = 0.0
        try:
            left_img_data_buffer = left_image.flatten()
            right_img_data_buffer = right_image.flatten()

            left_c_img_data_buffer = left_img_data_buffer.ctypes.data_as(
                POINTER(c_uint8)
            )
            right_c_img_data_buffer = right_img_data_buffer.ctypes.data_as(
                POINTER(c_uint8)
            )

            lim_height, lim_width, _ = left_image.shape
            lim_size = left_image.shape[1] * left_image.shape[0] * left_image.shape[2]

            rim_height, rim_width, _ = right_image.shape
            rim_size = (
                right_image.shape[1] * right_image.shape[0] * right_image.shape[2]
            )

            p_buffer_result = c_char_p()
            p_buffer_result_length = c_int()
            if config_object and config_object.get_config_param():
                c_config_param = c_char_p(
                    bytes(config_object.get_config_param(), "utf-8")
                )
                c_config_param_len = c_int(len(config_object.get_config_param()))
            else:
                c_config_param = c_char_p(bytes("", "utf-8"))
                c_config_param_len = c_int(0)
            success = self._spl_so_face.privid_face_compare_files(
                self._spl_so_face.handle,
                c_float(fudge_factor),
                c_config_param,
                c_config_param_len,
                left_c_img_data_buffer,
                c_int(lim_size),
                c_int(lim_width),
                c_int(lim_height),
                right_c_img_data_buffer,
                c_int(rim_size),
                c_int(rim_width),
                c_int(rim_height),
                byref(p_buffer_result),
                byref(p_buffer_result_length),
            )
            if not p_buffer_result.value or not p_buffer_result_length.value:
                raise Exception(
                    "Something went wrong. Please validate the images using isvalid function"
                )
            len_ = p_buffer_result_length.value
            output_json_str = p_buffer_result.value[:len_].decode()

            self._spl_so_face.privid_free_char_buffer(p_buffer_result)
            if output_json_str is not None and len(output_json_str) > 0:
                output = json.loads(output_json_str)
                # the status should receive the value of the success of the api call
                # according to FaceCompareResult (that is used in unit tests!!) comments and thus should have
                # * 0 : If successfully obtained result from server => API call success
                # * -1 : In case of error => API call failed
                # The 'result' in the other hand is a value returned by the operation
                #  which can be any basic type having any value
                output["status"] = 0 if success else -1
                return output
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def enroll(self, image_data: np.array, config_object: ConfigObject = None) -> Any:
        im_count = 1
        try:
            img_data = image_data
            im_height, im_width, im_channel = img_data.shape

            p_buffer_images_in = img_data
            c_p_buffer_images_in = p_buffer_images_in.ctypes.data_as(POINTER(c_uint8))
            im_size = im_height * im_width * im_channel
            p_buffer_embeddings_out = np.zeros(
                4 * self._embedding_length * self._num_embeddings, dtype=np.float32
            )
            c_p_buffer_embeddings_out = p_buffer_embeddings_out.ctypes.data_as(
                POINTER(c_float)
            )

            augmented_images = np.zeros(self._aug_size, dtype=np.int8)
            c_augmented_images = augmented_images.ctypes.data_as(POINTER(c_uint8))

            result_out = np.zeros(1, dtype=np.int32)
            c_result_out = result_out.ctypes.data_as(POINTER(ctypes.c_int32))
            c_result = c_char_p()
            emb_out_length = np.zeros(1, dtype=np.int32)
            c_emb_out_length = emb_out_length.ctypes.data_as(POINTER(ctypes.c_int32))

            augmented_images_length = np.zeros(1, dtype=np.int32)
            c_augmented_images_length = augmented_images_length.ctypes.data_as(
                POINTER(ctypes.c_int32)
            )

            if config_object and config_object.get_config_param():
                c_config_param = c_char_p(
                    bytes(config_object.get_config_param(), "utf-8")
                )
                c_config_param_len = c_int(len(config_object.get_config_param()))
            else:
                config_dict = {}
                config_dict["disable_enroll_mf"] = True
                c_config_param = c_char_p(bytes(json.dumps(config_dict), "utf-8"))
                c_config_param_len = c_int(len(json.dumps(config_dict)))

            best_input_out = c_uint8()  # uint8_t** best_input_out
            best_input_length = c_int()  # int *best_input_length
            self._spl_so_face.privid_enroll_onefa(
                self._spl_so_face.handle,
                c_config_param,
                c_config_param_len,
                c_p_buffer_images_in,
                c_int(im_count),
                c_int(im_size),
                c_int(im_width),
                c_int(im_height),
                byref(best_input_out),
                byref(best_input_length),
                byref(c_result),
                c_result_out,
            )

            len_ = np.fromiter(c_result_out[:1], dtype=np.uint32, count=-1)[0]
            output_json_str = c_result.value[:len_].decode()
            self._spl_so_face.privid_free_char_buffer(c_result)
            if output_json_str is not None and len(output_json_str) > 0:
                output = json.loads(output_json_str)
                return output
            return False
        except Exception as e:
            print("Error :", e)
            return False

    def predict(self, image_data: np.array, config_object: ConfigObject = None) -> Any:
        im_count = 1
        try:
            img_data = image_data
            im_height, im_width, im_channel = img_data.shape

            p_buffer_images_in = img_data
            c_p_buffer_images_in = p_buffer_images_in.ctypes.data_as(POINTER(c_uint8))
            im_size = im_height * im_width * im_channel
            p_buffer_embeddings_out = np.zeros(
                4 * self._embedding_length * self._num_embeddings, dtype=np.float32
            )
            c_p_buffer_embeddings_out = p_buffer_embeddings_out.ctypes.data_as(
                POINTER(c_float)
            )

            augmented_images = np.zeros(self._aug_size, dtype=np.int8)
            c_augmented_images = augmented_images.ctypes.data_as(POINTER(c_uint8))

            result_out = np.zeros(1, dtype=np.int32)
            c_result_out = result_out.ctypes.data_as(POINTER(ctypes.c_int32))

            emb_out_lenght = np.zeros(1, dtype=np.int32)
            emb_out_lenght = emb_out_lenght.ctypes.data_as(POINTER(ctypes.c_int32))
            c_result = c_char_p()
            augmented_images_length = np.zeros(1, dtype=np.int32)
            c_augmented_images_length = augmented_images_length.ctypes.data_as(
                POINTER(ctypes.c_int32)
            )
            if config_object and config_object.get_config_param():
                c_config_param = c_char_p(
                    bytes(config_object.get_config_param(), "utf-8")
                )
                c_config_param_len = c_int(len(config_object.get_config_param()))
            else:
                c_config_param = c_char_p(bytes("", "utf-8"))
                c_config_param_len = c_int(0)
            self._spl_so_face.privid_face_predict_onefa(
                self._spl_so_face.handle,
                c_config_param,
                c_config_param_len,
                c_p_buffer_images_in,
                c_int(im_count),
                c_int(im_size),
                c_int(im_width),
                c_int(im_height),
                byref(c_result),
                c_result_out,
            )
            len_ = np.fromiter(c_result_out[:1], dtype=np.uint32, count=-1)[0]
            output_json_str = c_result.value[:len_].decode()
            self._spl_so_face.privid_free_char_buffer(c_result)
            if output_json_str is not None and len(output_json_str) > 0:
                output = json.loads(output_json_str)
                return output
            return False
        except Exception as e:
            print("Error :", e)
            return False

    def antispoofing(
        self, image_data: np.array, config_object: ConfigObject = None
    ) -> Any:
        try:
            img = image_data
            im_width = img.shape[1]
            im_height = img.shape[0]

            p_buffer_images_in = img.flatten()
            c_p_buffer_images_in = p_buffer_images_in.ctypes.data_as(POINTER(c_uint8))

            c_result = c_char_p()
            c_result_len = c_int()
            if config_object and config_object.get_config_param():
                c_config_param = c_char_p(
                    bytes(config_object.get_config_param(), "utf-8")
                )
                c_config_param_len = c_int(len(config_object.get_config_param()))
            else:
                c_config_param = c_char_p(bytes("", "utf-8"))
                c_config_param_len = c_int(0)
            self._spl_so_face.privid_anti_spoofing(
                self._spl_so_face.handle,
                c_p_buffer_images_in,
                c_int(im_width),
                c_int(im_height),
                c_config_param,
                c_config_param_len,
                byref(c_result),
                byref(c_result_len),
            )

            if not c_result.value or not c_result_len.value:
                raise Exception(
                    "Something went wrong. Couldn't process the image for antispoofing API. "
                )
            output_json = c_result.value[: c_result_len.value].decode()
            self._spl_so_face.privid_free_char_buffer(c_result)

            output = json.loads(output_json)
            return output
        except Exception as e:
            print(e)
            return False
import ctypes
import json
import pathlib
import sys
from ctypes import *
from typing import Any

import numpy as np
from PIL import Image

from ..settings.cacheType import CacheType
from ..settings.configuration import ConfigObject
from ..settings.loggingLevel import LoggingLevel


class NativeMethods(object):
    def __init__(self, api_key: str, server_url: str, local_storage_path: str,
                 logging_level: LoggingLevel, tf_num_thread: int, cache_type: CacheType,
                 config_object: ConfigObject = None):
        try:
            self._config_object = config_object
            self._library_path = str(pathlib.Path(__file__).parent.joinpath("lib/lib_fhe.so").resolve())
            self._embedding_length = 128
            self._num_embeddings = 80
            self._aug_size = 224 * 224 * 4 * self._num_embeddings
            self._spl_so_face = None
            self._tf_num_thread = tf_num_thread
            self._api_key = bytes(api_key, 'utf-8')
            self._server_url = bytes(server_url, 'utf-8')
            self._logging_level = logging_level
            self._local_storage_path = local_storage_path
            self._cache_type = cache_type
            self._face_setup()
        except Exception as e:
            print("Error ", e)
            sys.exit(1)

    def update_config(self, config_object):
        self._config_object = config_object
        if self._config_object and self._config_object.get_config_param():
            c_config_param = c_char_p(bytes(self._config_object.get_config_param(), 'utf-8'))
            c_config_param_len = c_int(len(self._config_object.get_config_param()))
            self._spl_so_face.privid_set_configuration(self._spl_so_face.new_handle, c_config_param, c_config_param_len)

    def _face_setup(self):
        self._spl_so_face = ctypes.CDLL(self._library_path)

        # privid_global_settings
        self._spl_so_face.privid_global_settings.argtypes = [c_uint8, c_uint8]
        self._spl_so_face.privid_global_settings.restype = c_bool
        self._spl_so_face.privid_global_settings(self._tf_num_thread, self._logging_level.value)

        # FHE_init
        # self._spl_so_face._FHE_init = self._spl_so_face.FHE_init
        self._spl_so_face.FHE_init.argtypes = [c_int]
        self._spl_so_face.FHE_init.restype = POINTER(c_uint8)
        self._spl_so_face.handle = self._spl_so_face.FHE_init(self._logging_level.value)

        self._spl_so_face.privid_initialize_session_join.argtypes = [POINTER(c_void_p), c_void_p]
        self._spl_so_face.privid_initialize_session_join.restype = c_bool
        self._spl_so_face.new_handle = c_void_p()

        self._spl_so_face.privid_initialize_session_join(byref(self._spl_so_face.new_handle), self._spl_so_face.handle)

        # FHE_configure_url
        # self._spl_so_face.FHE_configure_url = self._spl_so_face.FHE_configure_url
        self._spl_so_face.FHE_configure_url.argtypes = [
            POINTER(c_uint8), c_int, c_char_p, c_int]
        self._spl_so_face.FHE_configure_url.restype = c_uint8

        # privid_set_configuration
        self._spl_so_face.privid_set_configuration.argtypes = [c_void_p, c_char_p, c_int]
        self._spl_so_face.privid_set_configuration.restype = c_bool

        # configure_url , API key and storage location
        self._spl_so_face.FHE_configure_url(self._spl_so_face.handle, c_int32(46),
                                            c_char_p(self._api_key),
                                            c_int32(len(self._api_key)))

        self._spl_so_face.FHE_configure_url(self._spl_so_face.handle, c_int32(42),
                                            c_char_p(self._server_url),
                                            c_int32(len(self._server_url)))

        # Configure parameters 
        if self._config_object and self._config_object.get_config_param():
            config_dict = json.loads(self._config_object.get_config_param())
            config_dict["cache_type"] = self._cache_type.value
            config_dict["local_storage_path"] = self._local_storage_path
            config_dict = json.dumps(config_dict)
            c_config_param = c_char_p(bytes(config_dict, 'utf-8'))
            c_config_param_len = c_int(len(config_dict))
            self._spl_so_face.privid_set_configuration(self._spl_so_face.new_handle, c_config_param, c_config_param_len)
        # self._spl_so_face.privid_set_configuration.restype = c_int
        # FHE_close
        # self._spl_so_face.FHE_close = self._spl_so_face.FHE_close
        self._spl_so_face.FHE_close.argtypes = [POINTER(c_uint8)]
        self._spl_so_face.FHE_close.restype = c_int

        # privid_enroll_onefa
        # self._spl_so_face.privid_enroll_onefa = self._spl_so_face.privid_enroll_onefa
        self._spl_so_face.privid_enroll_onefa.argtypes = [c_void_p, c_char_p, c_int, POINTER(
            c_uint8), c_int, c_int, c_int, c_int, POINTER(c_float), POINTER(c_int), c_bool, POINTER(c_uint8),
                                                          POINTER(c_int), POINTER(c_char_p),
                                                          POINTER(c_int)]
        self._spl_so_face.privid_enroll_onefa.restype = c_int

        # privid_face_predict_onefa
        # self._spl_so_face.privid_face_predict_onefa = self._spl_so_face.privid_face_predict_onefa
        self._spl_so_face.privid_face_predict_onefa.argtypes = [c_void_p, c_char_p, c_int, POINTER(
            c_uint8), c_int, c_int, c_int, c_int, POINTER(c_float), POINTER(c_int), c_bool, POINTER(c_uint8),
                                                                POINTER(c_int), POINTER(c_char_p),
                                                                POINTER(c_int)]
        self._spl_so_face.privid_face_predict_onefa.restype = c_int

        # is_valid
        # self._spl_so_face.is_valid = self._spl_so_face.is_valid
        self._spl_so_face.is_valid.argtypes = [POINTER(c_uint8), c_bool, POINTER(
            c_uint8), c_int, c_int, POINTER(c_uint8), POINTER(c_int), POINTER(c_char_p), POINTER(c_int),
                                               POINTER(c_char_p), c_int]
        self._spl_so_face.is_valid.restype = c_int

        # FHE_delete
        # self._spl_so_face.privid_user_delete = self._spl_so_face.privid_user_delete
        self._spl_so_face.privid_user_delete.argtypes = [c_void_p, POINTER(c_char), c_int, POINTER(
            c_char), c_int, POINTER(c_char_p), POINTER(c_int)]
        self._spl_so_face.privid_user_delete.restype = c_int

        # FHE_free_api_memory
        # self._spl_so_face.FHE_free_api_memory = self._spl_so_face.FHE_free_api_memory
        self._spl_so_face.FHE_free_api_memory.argtypes = [POINTER(c_char_p)]

        # FHE_compare_files
        # self._spl_so_face.privid_face_compare_files = self._spl_so_face.privid_face_compare_files
        self._spl_so_face.privid_face_compare_files.argtypes = [c_void_p, c_float, c_char_p, c_int,
                                                                POINTER(c_uint8), c_int, c_int, c_int,
                                                                POINTER(c_uint8), c_int, c_int, c_int,
                                                                POINTER(c_char_p),
                                                                POINTER(c_int)]
        self._spl_so_face.privid_face_compare_files.restype = c_int

        # privid_validate
        self._spl_so_face.privid_validate.argtypes = [
            c_void_p, POINTER(c_uint8), c_int, c_int,
            c_char_p, c_int, POINTER(c_char_p), POINTER(c_int)]
        self._spl_so_face.privid_validate.restype = c_bool

        # privid_estimate_age
        self._spl_so_face.privid_estimate_age.argtypes = [
            c_void_p, POINTER(c_uint8), c_int, c_int,
            c_char_p, c_int, POINTER(c_char_p), POINTER(c_int)]
        self._spl_so_face.privid_estimate_age.restype = c_bool

        # privid_face_iso
        self._spl_so_face.privid_face_iso.argtypes = [
            c_void_p, POINTER(c_uint8), c_int, c_int,
            c_char_p, c_int, POINTER(c_char_p), POINTER(c_int),
            POINTER(POINTER(c_ubyte)), POINTER(c_int)]
        self._spl_so_face.privid_estimate_age.restype = c_bool

    def is_valid(self, image_data: np.array, is_enroll: bool = False, config_object: ConfigObject = None) -> Any:
        try:
            img = image_data
            im_width = img.shape[1]
            im_height = img.shape[0]
            p_buffer_images_in = img.flatten()
            c_p_buffer_images_in = p_buffer_images_in.ctypes.data_as(
                POINTER(c_uint8))
            p_buffer_embeddings_out = np.zeros(224 * 224 * 4, dtype=np.int8)
            c_p_buffer_embeddings_out = p_buffer_embeddings_out.ctypes.data_as(
                POINTER(c_uint8))

            result_out = np.zeros(1, dtype=np.int32)
            c_result_out = result_out.ctypes.data_as(POINTER(ctypes.c_int32))

            buffer_embeddings_out_length = np.zeros(1, dtype=np.int32)
            c_buffer_embeddings_out_length = buffer_embeddings_out_length.ctypes.data_as(POINTER(ctypes.c_int32))

            c_result = c_char_p()
            self._spl_so_face.is_valid(self._spl_so_face.handle, c_bool(is_enroll), c_p_buffer_images_in,
                                       c_int(im_width),
                                       c_int(im_height), c_p_buffer_embeddings_out,
                                       c_buffer_embeddings_out_length, byref(c_result), c_result_out,
                                       c_char_p(), c_int(0))

            len_ = np.fromiter(c_result_out[:1], dtype=np.uint32, count=-1)[0]
            output_json = c_result.value[:len_].decode()
            self._spl_so_face.FHE_free_api_memory(byref(c_result))
            output = json.loads(output_json)
            return output
        except Exception as e:
            print(e)
            return False

    def is_valid_without_age(self, image_data: np.array, config_object: ConfigObject = None) -> Any:
        try:
            img = image_data
            im_width = img.shape[1]
            im_height = img.shape[0]

            p_buffer_images_in = img.flatten()
            c_p_buffer_images_in = p_buffer_images_in.ctypes.data_as(POINTER(c_uint8))

            c_result = c_char_p()
            c_result_len = c_int()
            if config_object and config_object.get_config_param():
                c_config_param = c_char_p(bytes(config_object.get_config_param(), 'utf-8'))
                c_config_param_len = c_int(len(config_object.get_config_param()))
            else:
                c_config_param = c_char_p(bytes("", 'utf-8'))
                c_config_param_len = c_int(0)
            self._spl_so_face.privid_validate(
                self._spl_so_face.new_handle, c_p_buffer_images_in, c_int(im_width), c_int(im_height),
                c_config_param, c_config_param_len,
                byref(c_result), byref(c_result_len))

            if not c_result.value or not c_result_len.value:
                raise Exception("Something went wrong. Couldn't process the image for is_valid API. ")
            output_json = c_result.value[:c_result_len.value].decode()
            self._spl_so_face.FHE_free_api_memory(c_result)

            output = json.loads(output_json)
            return output
        except Exception as e:
            print(e)
            return False

    def estimate_age(self, image_data: np.array, config_object: ConfigObject = None) -> Any:
        try:
            img = image_data
            im_width = img.shape[1]
            im_height = img.shape[0]

            p_buffer_images_in = img.flatten()
            c_p_buffer_images_in = p_buffer_images_in.ctypes.data_as(POINTER(c_uint8))

            c_result = c_char_p()
            c_result_len = c_int()
            if config_object and config_object.get_config_param():
                c_config_param = c_char_p(bytes(config_object.get_config_param(), 'utf-8'))
                c_config_param_len = c_int(len(config_object.get_config_param()))
            else:
                c_config_param = c_char_p(bytes("", 'utf-8'))
                c_config_param_len = c_int(0)
            self._spl_so_face.privid_estimate_age(
                self._spl_so_face.new_handle, c_p_buffer_images_in, c_int(im_width), c_int(im_height),
                c_config_param, c_config_param_len,
                byref(c_result), byref(c_result_len))

            if not c_result.value or not c_result_len.value:
                raise Exception("Something went wrong. Couldn't process the image for estimate_age API. ")
            output_json = c_result.value[:c_result_len.value].decode()
            self._spl_so_face.FHE_free_api_memory(c_result)

            output = json.loads(output_json)
            return output
        except Exception as e:
            print(e)
            return False

    def get_iso_face(self, image_data: np.array, config_object: ConfigObject = None) -> Any:
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
                c_config_param = c_char_p(bytes(config_object.get_config_param(), 'utf-8'))
                c_config_param_len = c_int(len(config_object.get_config_param()))
            else:
                c_config_param = c_char_p(bytes("", 'utf-8'))
                c_config_param_len = c_int(0)

            self._spl_so_face.privid_face_iso(
                self._spl_so_face.new_handle, c_p_buffer_images_in, c_int(im_width), c_int(im_height),
                c_config_param, c_config_param_len,
                byref(c_result), byref(c_result_len), byref(c_iso_image), byref(c_iso_image_len))

            if not c_result.value or not c_result_len.value:
                raise Exception("Something went wrong. Couldn't process the image for get_iso_face API. ")
            output_json = c_result.value[:c_result_len.value].decode()
            output_json = json.loads(output_json)
            self._spl_so_face.FHE_free_api_memory(c_result)
            if c_iso_image_len.value and "iso_image_width" in output_json and "iso_image_height" in output_json:
                output_json["image"] = Image.fromarray(np.uint8(np.reshape(c_iso_image[:c_iso_image_len.value], (
                    output_json.get("iso_image_height", 0), output_json.get("iso_image_width", 0),
                    output_json.get("iso_image_channels", 0))))).convert(
                    "RGBA" if output_json.get("iso_image_channels", 0) == 4 else "RGB")
            else:
                # Empty Image
                output_json["image"] = Image.new("RGB", (800, 1280), (255, 255, 255))
            return output_json
        except Exception as e:
            print(e)
            return False

    def delete(self, uuid: str) -> Any:
        uuid = bytes(uuid, 'utf-8')
        p_buffer_result = c_char_p()
        p_buffer_result_length = c_int()
        c_config_param = c_char_p(bytes("", 'utf-8'))
        c_config_param_len = c_int(0)
        self._spl_so_face.privid_user_delete(self._spl_so_face.new_handle, c_config_param, c_config_param_len,
                                             c_char_p(uuid),
                                             c_int(
                                                 len(uuid)), byref(p_buffer_result),
                                             byref(p_buffer_result_length))

        len_ = p_buffer_result_length.value
        output_json_str = p_buffer_result.value[:len_].decode()

        self._spl_so_face.FHE_free_api_memory(byref(p_buffer_result))

        if output_json_str is not None and len(output_json_str) > 0:
            output = json.loads(output_json_str)
            return output
        else:
            return False

    def compare_files(self, left_image: np.array, right_image: np.array, config_object: ConfigObject = None) -> Any:
        fudge_factor = 0.0
        try:
            left_img_data_buffer = left_image.flatten()
            right_img_data_buffer = right_image.flatten()

            left_c_img_data_buffer = left_img_data_buffer.ctypes.data_as(
                POINTER(c_uint8))
            right_c_img_data_buffer = right_img_data_buffer.ctypes.data_as(
                POINTER(c_uint8))

            lim_height, lim_width, _ = left_image.shape
            lim_size = left_image.shape[1] * left_image.shape[0] * left_image.shape[2]

            rim_height, rim_width, _ = right_image.shape
            rim_size = right_image.shape[1] * right_image.shape[0] * right_image.shape[2]

            p_buffer_result = c_char_p()
            p_buffer_result_length = c_int()
            if config_object and config_object.get_config_param():
                c_config_param = c_char_p(bytes(config_object.get_config_param(), 'utf-8'))
                c_config_param_len = c_int(len(config_object.get_config_param()))
            else:
                c_config_param = c_char_p(bytes("", 'utf-8'))
                c_config_param_len = c_int(0)
            self._spl_so_face.privid_face_compare_files(self._spl_so_face.new_handle, c_float(fudge_factor),
                                                        c_config_param,
                                                        c_config_param_len,
                                                        left_c_img_data_buffer,
                                                        c_int(lim_size), c_int(lim_width), c_int(lim_height),
                                                        right_c_img_data_buffer, c_int(rim_size),
                                                        c_int(rim_width), c_int(rim_height),
                                                        byref(p_buffer_result), byref(p_buffer_result_length))
            if not p_buffer_result.value or not p_buffer_result_length.value:
                raise Exception("Something went wrong. Please validate the images using isvalid function")
            len_ = p_buffer_result_length.value
            output_json_str = p_buffer_result.value[:len_].decode()

            self._spl_so_face.FHE_free_api_memory(byref(p_buffer_result))
            if output_json_str is not None and len(output_json_str) > 0:
                output = json.loads(output_json_str)
                output["status"] = output["result"]
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
            c_p_buffer_images_in = p_buffer_images_in.ctypes.data_as(
                POINTER(c_uint8))
            im_size = im_height * im_width * im_channel
            p_buffer_embeddings_out = np.zeros(
                4 * self._embedding_length * self._num_embeddings, dtype=np.float32)
            c_p_buffer_embeddings_out = p_buffer_embeddings_out.ctypes.data_as(
                POINTER(c_float))

            augmented_images = np.zeros(self._aug_size, dtype=np.int8)
            c_augmented_images = augmented_images.ctypes.data_as(
                POINTER(c_uint8))

            result_out = np.zeros(1, dtype=np.int32)
            c_result_out = result_out.ctypes.data_as(POINTER(ctypes.c_int32))
            c_result = c_char_p()
            emb_out_length = np.zeros(1, dtype=np.int32)
            c_emb_out_length = emb_out_length.ctypes.data_as(POINTER(ctypes.c_int32))

            augmented_images_length = np.zeros(1, dtype=np.int32)
            c_augmented_images_length = augmented_images_length.ctypes.data_as(POINTER(ctypes.c_int32))
            if config_object and config_object.get_config_param():
                c_config_param = c_char_p(bytes(config_object.get_config_param(), 'utf-8'))
                c_config_param_len = c_int(len(config_object.get_config_param()))
            else:
                c_config_param = c_char_p(bytes("", 'utf-8'))
                c_config_param_len = c_int(0)
            self._spl_so_face.privid_enroll_onefa(self._spl_so_face.new_handle, c_config_param, c_config_param_len,
                                                  c_p_buffer_images_in,
                                                  c_int(im_count), c_int(im_size), c_int(im_width),
                                                  c_int(im_height),
                                                  c_p_buffer_embeddings_out, c_emb_out_length, c_bool(True),
                                                  c_augmented_images, c_augmented_images_length,
                                                  byref(c_result), c_result_out)

            len_ = np.fromiter(c_result_out[:1], dtype=np.uint32, count=-1)[0]
            output_json_str = c_result.value[:len_].decode()
            self._spl_so_face.FHE_free_api_memory(byref(c_result))
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
            c_p_buffer_images_in = p_buffer_images_in.ctypes.data_as(
                POINTER(c_uint8))
            im_size = im_height * im_width * im_channel
            p_buffer_embeddings_out = np.zeros(
                4 * self._embedding_length * self._num_embeddings, dtype=np.float32)
            c_p_buffer_embeddings_out = p_buffer_embeddings_out.ctypes.data_as(
                POINTER(c_float))

            augmented_images = np.zeros(self._aug_size, dtype=np.int8)
            c_augmented_images = augmented_images.ctypes.data_as(
                POINTER(c_uint8))

            result_out = np.zeros(1, dtype=np.int32)
            c_result_out = result_out.ctypes.data_as(POINTER(ctypes.c_int32))

            emb_out_lenght = np.zeros(1, dtype=np.int32)
            emb_out_lenght = emb_out_lenght.ctypes.data_as(POINTER(ctypes.c_int32))
            c_result = c_char_p()
            augmented_images_length = np.zeros(1, dtype=np.int32)
            c_augmented_images_length = augmented_images_length.ctypes.data_as(POINTER(ctypes.c_int32))
            if config_object and config_object.get_config_param():
                c_config_param = c_char_p(bytes(config_object.get_config_param(), 'utf-8'))
                c_config_param_len = c_int(len(config_object.get_config_param()))
            else:
                c_config_param = c_char_p(bytes("", 'utf-8'))
                c_config_param_len = c_int(0)
            self._spl_so_face.privid_face_predict_onefa(self._spl_so_face.new_handle, c_config_param,
                                                        c_config_param_len,
                                                        c_p_buffer_images_in,
                                                        c_int(im_count), c_int(im_size), c_int(im_width),
                                                        c_int(im_height),
                                                        c_p_buffer_embeddings_out, emb_out_lenght, c_bool(True),
                                                        c_augmented_images, c_augmented_images_length, byref(c_result),
                                                        c_result_out)
            len_ = np.fromiter(c_result_out[:1], dtype=np.uint32, count=-1)[0]
            output_json_str = c_result.value[:len_].decode()
            self._spl_so_face.FHE_free_api_memory(byref(c_result))
            if output_json_str is not None and len(output_json_str) > 0:
                output = json.loads(output_json_str)
                return output
            return False
        except Exception as e:
            print("Error :", e)
            return False

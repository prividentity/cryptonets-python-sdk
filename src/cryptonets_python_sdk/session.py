import os
from typing import Tuple, Any
import numpy as np
import msgspec
from cryptonets_python_sdk.library import PrivIDFaceLib, PrivIDError
from cryptonets_python_sdk.img_utils import ImageUtils
from cryptonets_python_sdk.idl.gen.privateid_types import (
    CallResult,
    SessionSettings,
    OperationConfig,
)


class ImageInputArg:
    """Class representing an image input argument.
    Can be initialized with either a file path or a numpy array.
    """
    image_format: str
    image_data: bytes
    width: int
    height: int
    orientation: int

    def __init__(self, image_in, image_format: str, apply_rotation: bool = True):
        ImageUtils.check_image_format(image_format)
        self.image_array = None
        if isinstance(image_in, str):
            self.image_array, self.image_format = ImageUtils.image_path_to_numpy_array(image_in, image_format,
                                                                                       apply_rotation)
            ImageUtils.check_image_array(self.image_array, self.image_format)
            self.width = self.image_array.shape[1]
            self.height = self.image_array.shape[0]
            self.image_data = self.image_array.tobytes()
            self.orientation = 1
        elif isinstance(image_in, np.ndarray):
            self.image_array = image_in
            if image_format == '':
                raise ValueError("Image format should not be empty when using numpy array")
            self.image_format = image_format.lower()
            ImageUtils.check_image_array(self.image_array, self.image_format)
            self.width = self.image_array.shape[1]
            self.height = self.image_array.shape[0]
            self.image_data = self.image_array.tobytes()
            self.orientation = 1
        else:
            raise ValueError("Invalid image input type")

    def __del__(self):
        if self.image_array is not None:
            del self.image_array
            self.image_array = None
        self.image_format = None
        self.image_data = None
        self.width = None
        self.height = None
        self.orientation = None


class SessionError(PrivIDError):
    """Exception for session-related errors"""
    pass


class SessionNative:
    """Native session for face recognition operations (internal use only).

    This class directly wraps the native C library and accepts JSON strings or bytes.
    External code should use the Session class which provides a typed interface.
    """

    def __init__(self, settings: str | bytes):
        """Initialize a native session

        Args:
            settings: Session settings as JSON string or UTF-8 encoded bytes
        Note:
            This constructor is intended for internal use only.
            External code should use Session class instead.
        """
        if not PrivIDFaceLib.is_initialized():
            raise SessionError("PrivIDFaceLib is not initialized. Call PrivIDFaceLib.initialize() first.")
        self._lib = PrivIDFaceLib._lib
        self._ffibuilder = PrivIDFaceLib._ffibuilder
        self._session = None

        # Convert settings to bytes if needed
        if isinstance(settings, str):
            settings_bytes = settings.encode('utf-8')
        elif isinstance(settings, bytes):
            settings_bytes = settings
        else:
            raise TypeError(f"settings must be str or bytes, got {type(settings).__name__}")

        settings_len = len(settings_bytes)

        # Create a pointer to store the session pointer
        session_ptr = self._ffibuilder.new('void **')

        # Initialize the session
        if not self._lib.privid_initialize_session(settings_bytes, settings_len, session_ptr):
            raise SessionError("Failed to initialize session")

        if not session_ptr[0]:
            raise SessionError("Failed to initialize session: No session pointer returned")

        # Store the session pointer
        self._session = session_ptr[0]

    def __del__(self):
        """Cleanup when session is destroyed"""
        if self._session:
            self._lib.privid_deinitialize_session(self._session)
            self._session = None

    def _validate(self, image_bytes: bytes, image_width: int, image_height: int, user_config_bytes: bytes = b"") -> \
    tuple[int, str]:
        """Internal method to validate a face image

        Args:
            image_bytes: Image data as bytes
            image_width: Image width
            image_height: Image height
            user_config_bytes: JSON configuration as UTF-8 encoded bytes
        """
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_validate(
            self._session,
            user_config_bytes, len(user_config_bytes),
            image_bytes, image_width, image_height,
            result_ptr, result_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        self._lib.privid_free_char_buffer(result_ptr[0])
        return op_id, result

    def validate(self, image_input: ImageInputArg, user_config: str = "") -> tuple[int, str]:
        """Validate a face image using ImageInputArg"""
        config_bytes = user_config.encode('utf-8')
        return self._validate(image_input.image_data, image_input.width, image_input.height, config_bytes)

    def _face_iso(self, image_bytes: bytes, width: int, height: int, user_config_bytes: bytes = b"") -> tuple[
        int, str, bytes]:
        """Internal method to process face image according to ISO standards

        Args:
            image_bytes: Image data as bytes
            width: Image width
            height: Image height
            user_config_bytes: JSON configuration as UTF-8 encoded bytes
        """
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')
        iso_image_ptr = self._ffibuilder.new('uint8_t **')
        iso_image_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_face_iso(
            self._session,
            user_config_bytes, len(user_config_bytes),
            image_bytes, width, height,
            iso_image_ptr, iso_image_len,
            result_ptr, result_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        iso_image = self._ffibuilder.buffer(iso_image_ptr[0], iso_image_len[0])
        iso_bytes = bytes(iso_image)

        self._lib.privid_free_char_buffer(result_ptr[0])
        self._lib.privid_free_buffer(iso_image_ptr[0])

        return op_id, result, iso_bytes

    def face_iso(self, image_input: ImageInputArg, user_config: str = "") -> tuple[int, str, bytes]:
        """Process face image according to ISO standards using ImageInputArg"""
        config_bytes = user_config.encode('utf-8')
        return self._face_iso(image_input.image_data, image_input.width, image_input.height, config_bytes)

    def _anti_spoofing(self, image_bytes: bytes, width: int, height: int, user_config_bytes: bytes = b"") -> tuple[
        int, str]:
        """Internal method for anti-spoofing detection on a face image

        Args:
            image_bytes: Image data as bytes
            width: Image width
            height: Image height
            user_config_bytes: JSON configuration as UTF-8 encoded bytes
        """
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')
        op_id = self._lib.privid_anti_spoofing(
            self._session,
            user_config_bytes, len(user_config_bytes),
            image_bytes, width, height,
            result_ptr, result_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')

        self._lib.privid_free_char_buffer(result_ptr[0])

        return op_id, result

    def anti_spoofing(self, image_input: ImageInputArg, user_config: str = "") -> tuple[int, str]:
        """Perform anti-spoofing detection on a face image using ImageInputArg"""
        config_bytes = user_config.encode('utf-8')
        return self._anti_spoofing(image_input.image_data, image_input.width, image_input.height, config_bytes)

    def _face_compare_files(self, user_config_bytes: bytes,
                            image_a: bytes, image_a_width: int, image_a_height: int,
                            image_b: bytes, image_b_width: int, image_b_height: int) -> tuple[int, str]:
        """Internal method to compare two face images

        Args:
            user_config_bytes: JSON configuration as UTF-8 encoded bytes
            image_a: First image data as bytes
            image_a_width: First image width
            image_a_height: First image height
            image_b: Second image data as bytes
            image_b_width: Second image width
            image_b_height: Second image height
        """
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_face_compare_files(
            self._session,
            user_config_bytes, len(user_config_bytes),
            image_a, image_a_width, image_a_height,
            image_b, image_b_width, image_b_height,
            result_ptr, result_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        self._lib.privid_free_char_buffer(result_ptr[0])

        return op_id, result

    def face_compare_files(self, user_config: str,
                           image_a: ImageInputArg, image_b: ImageInputArg) -> tuple[int, str]:
        """Compare two face images using ImageInputArg

        Args:
            user_config: JSON configuration string
            image_a: First face image to compare
            image_b: Second face image to compare

        Returns:
            tuple[int, str]: Status code and JSON result containing comparison data
        """
        config_bytes = user_config.encode('utf-8')
        return self._face_compare_files(
            config_bytes,
            image_a.image_data, image_a.width, image_a.height,
            image_b.image_data, image_b.width, image_b.height
        )

    def _doc_scan_face(self, user_config_bytes: bytes, image: bytes, width: int, height: int) -> tuple[
        int, str, bytes, bytes]:
        """Internal method to scan a document for face and extract it

        Args:
            user_config_bytes: JSON configuration as UTF-8 encoded bytes
            image: Image data as bytes
            width: Image width
            height: Image height
        """
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')
        doc_ptr = self._ffibuilder.new('uint8_t **')
        doc_len = self._ffibuilder.new('int *')
        face_ptr = self._ffibuilder.new('uint8_t **')
        face_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_doc_scan_face(
            self._session,
            user_config_bytes, len(user_config_bytes),
            image, width, height,
            doc_ptr, doc_len,
            face_ptr, face_len,
            result_ptr, result_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        doc = self._ffibuilder.buffer(doc_ptr[0], doc_len[0])
        doc_bytes = bytes(doc)
        face = self._ffibuilder.buffer(face_ptr[0], face_len[0])
        face_bytes = bytes(face)

        self._lib.privid_free_char_buffer(result_ptr[0])
        self._lib.privid_free_buffer(doc_ptr[0])
        self._lib.privid_free_buffer(face_ptr[0])

        return op_id, result, doc_bytes, face_bytes

    def doc_scan_face(self, user_config: str, image: ImageInputArg) -> tuple[int, str, bytes, bytes]:
        """Scan a document for face and extract it using ImageInputArg"""
        config_bytes = user_config.encode('utf-8')
        return self._doc_scan_face(config_bytes, image.image_data, image.width, image.height)

    def _estimate_age(self, image_bytes: bytes, width: int, height: int, user_config_bytes: bytes = b"") -> tuple[
        int, str]:
        """Internal method to estimate age from a face image

        Args:
            image_bytes: Image data as bytes
            width: Image width
            height: Image height
            user_config_bytes: JSON configuration as UTF-8 encoded bytes
        """
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_estimate_age(
            self._session,
            user_config_bytes, len(user_config_bytes),
            image_bytes, width, height,
            result_ptr, result_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        self._lib.privid_free_char_buffer(result_ptr[0])
        return op_id, result

    def estimate_age(self, image_input: ImageInputArg, user_config: str = "") -> tuple[int, str]:
        """Estimate age from a face image using ImageInputArg"""
        config_bytes = user_config.encode('utf-8')
        return self._estimate_age(image_input.image_data, image_input.width, image_input.height, config_bytes)

    def _enroll_onefa(self, user_config_bytes: bytes, images: bytes,
                      image_width: int, image_height: int) -> tuple[int, str]:
        """Internal method to enroll one or more face images

        Args:
            user_config_bytes: JSON configuration as UTF-8 encoded bytes
            images: Image data as bytes
            image_width: Image width
            image_height: Image height

        Note: The new API signature no longer returns best_input image or requires image_count.
        """
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_enroll_onefa(
            self._session,
            user_config_bytes, len(user_config_bytes),
            images, image_width, image_height,
            result_ptr, result_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        self._lib.privid_free_char_buffer(result_ptr[0])

        return op_id, result

    def enroll_onefa(self, user_config: str, image_input: ImageInputArg) -> tuple[int, str]:
        """Enroll a face image using ImageInputArg

        Args:
            user_config: JSON configuration string
            image_input: ImageInputArg containing the face image

        Returns:
            tuple[int, str]: Status code and JSON result containing enrollment data
        """
        config_bytes = user_config.encode('utf-8')
        return self._enroll_onefa(config_bytes, image_input.image_data, image_input.width, image_input.height)

    def _face_predict_onefa(self, user_config_bytes: bytes, images: bytes,
                            image_width: int, image_height: int) -> tuple[int, str]:
        """Internal method to predict using enrolled face images

        Args:
            user_config_bytes: JSON configuration as UTF-8 encoded bytes
            images: Image data as bytes
            image_width: Image width
            image_height: Image height
        """
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_face_predict_onefa(
            self._session,
            user_config_bytes, len(user_config_bytes),
            images, image_width, image_height,
            result_ptr, result_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        self._lib.privid_free_char_buffer(result_ptr[0])
        return op_id, result

    def face_predict_onefa(self, user_config: str, image_input: ImageInputArg) -> tuple[int, str]:
        """Predict using enrolled face image using ImageInputArg

        Args:
            user_config: JSON configuration string
            image_input: ImageInputArg containing the face image

        Returns:
            tuple[int, str]: Status code and JSON result containing prediction data
        """
        config_bytes = user_config.encode('utf-8')
        return self._face_predict_onefa(config_bytes, image_input.image_data, image_input.width, image_input.height)

    def _user_delete(self, user_config_bytes: bytes, puid_bytes: bytes) -> tuple[int, str]:
        """Internal method to delete a user by PUID

        Args:
            user_config_bytes: JSON configuration as UTF-8 encoded bytes
            puid_bytes: PUID as UTF-8 encoded bytes
        """
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_user_delete(
            self._session, user_config_bytes, len(user_config_bytes),
            puid_bytes, len(puid_bytes),
            result_ptr, result_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        self._lib.privid_free_char_buffer(result_ptr[0])
        return op_id, result

    def user_delete(self, user_config: str, puid: str) -> tuple[int, str]:
        """Delete a user by PUID

        Args:
            user_config: JSON configuration string
            puid: User's unique identifier to delete

        Returns:
            tuple[int, str]: Status code and JSON result containing deletion status
        """
        config_bytes = user_config.encode('utf-8')
        puid_bytes = puid.encode('utf-8')
        return self._user_delete(config_bytes, puid_bytes)


class Session:
    """Type-safe session class for face recognition operations.

    This class provides a typed interface using msgspec Struct types.
    It wraps `SessionNative`, which handles the actual native library calls.
    When the class is initialized, `msgspec` encoders and decoders are created.

    Raises:
        SessionError: If msgspec encoders or decoders creation fails.
    """

    # Class-level encoder/decoders - reused across all instances for performance
    # One encoder suffices for all types (stateless and thread-safe)
    # Multiple decoders needed - one per type since decoders are typed

    try:
        _encoder = msgspec.json.Encoder()
        _result_decoder = msgspec.json.Decoder(CallResult)
    except Exception as e:
        raise SessionError(f"Failed to create msgspec encoder/decoder: {e}")

    def __init__(self, settings: SessionSettings):
        """Initialize a session with typed settings.

        Args:
            settings: SessionSettings struct containing collections, token, etc.

        Raises:
            SessionError: If session initialization fails
        """
        self._session_native: SessionNative = None

        # Convert typed settings to JSON bytes for native session using class-level encoder
        settings_bytes = Session._encoder.encode(settings)

        # Create native session (passes bytes directly, avoiding unnecessary decode/encode)
        self._session_native = SessionNative(settings_bytes)

    @classmethod
    def from_json(cls, settings_json: str) -> 'Session':
        """Alternative constructor from JSON string.

        Args:
            settings_json: JSON string containing session settings

        Returns:
            New Session instance

        Raises:
            msgspec.ValidationError: If JSON doesn't match SessionSettings schema
        """
        settings_decoder = msgspec.json.Decoder(SessionSettings)
        settings = settings_decoder.decode(settings_json.encode('utf-8'))
        return cls(settings)

    @classmethod
    def from_dict(cls, settings_dict: dict) -> 'Session':
        """Alternative constructor from dictionary.

        Args:
            settings_dict: Dictionary containing session settings

        Returns:
            New Session instance

        Raises:
            msgspec.ValidationError: If dict doesn't match SessionSettings schema
        """
        settings = msgspec.convert(settings_dict, SessionSettings)
        return cls(settings)

    def validate(
            self,
            image: ImageInputArg,
            config: OperationConfig
    ) -> Tuple[int, CallResult]:
        """Validate a face image with typed configuration.

        Detects face, checks quality, estimates pose, and performs anti-spoofing.

        Args:
            image: Input image (path or numpy array wrapped in ImageInputArg)
            config: Typed operation configuration

        Returns:
            Tuple of (operation_id, typed_result)
            - operation_id: Positive on success, negative on error
            - typed_result: CallResult with faces, status, and metadata

        """
        config.input_image_format = image.image_format
        config_bytes = Session._encoder.encode(config)

        # Call native session
        op_id, result_json = self._session_native._validate(image.image_data, image.width, image.height, config_bytes)

        # Decode result to typed object
        result = Session._result_decoder.decode(result_json.encode('utf-8'))

        return op_id, result

    def enroll_onefa(
            self,
            image: ImageInputArg,
            config: OperationConfig
    ) -> Tuple[int, CallResult]:
        """Enroll a face image with typed configuration.

        Enrolls a face for 1FA authentication. Returns PUID on success.

        Args:
            image: Input face image
            config: Typed operation configuration

        Returns:
            Tuple of (operation_id, typed_result)
            - operation_id: Positive on success, negative on error
            - typed_result: CallResult with enrollment data (PUID, conf_token)

        """
        config.input_image_format = image.image_format
        config_bytes = Session._encoder.encode(config)
        op_id, result_json = self._session_native._enroll_onefa(config_bytes, image.image_data, image.width,
                                                                image.height)
        result = Session._result_decoder.decode(result_json.encode('utf-8'))
        return op_id, result

    def face_predict_onefa(
            self,
            image: ImageInputArg,
            config: OperationConfig
    ) -> Tuple[int, CallResult]:
        """Predict/authenticate using enrolled face with typed configuration.

        Matches face against enrolled faces in collection. Returns PUID and score.

        Args:
            image: Input face image to authenticate
            config: Typed operation configuration

        Returns:
            Tuple of (operation_id, typed_result)
            - operation_id: Positive on success, negative on error
            - typed_result: CallResult with prediction data (match, confidence, PUID)

        """
        config.input_image_format = image.image_format
        config_bytes = Session._encoder.encode(config)
        op_id, result_json = self._session_native._face_predict_onefa(config_bytes, image.image_data, image.width,
                                                                      image.height)
        result = Session._result_decoder.decode(result_json.encode('utf-8'))
        return op_id, result

    def face_compare_files(
            self,
            image_a: ImageInputArg,
            image_b: ImageInputArg,
            config: OperationConfig
    ) -> Tuple[int, CallResult]:
        """Compare two face images with typed configuration.

        Performs 1:1 face comparison. Returns similarity score and match result.

        Args:
            image_a: First face image
            image_b: Second face image
            config: Typed operation configuration

        Returns:
            Tuple of (operation_id, typed_result)
            - operation_id: Positive on success, negative on error
            - typed_result: CallResult with comparison data (similarity, is_match)

        """
        config.input_image_format = image_a.image_format
        config_bytes = Session._encoder.encode(config)
        op_id, result_json = self._session_native._face_compare_files(
            config_bytes, image_a.image_data, image_a.width, image_a.height, image_b.image_data, image_b.width,
            image_b.height
        )
        result = Session._result_decoder.decode(result_json.encode('utf-8'))
        return op_id, result

    def estimate_age(
            self,
            image: ImageInputArg,
            config: OperationConfig
    ) -> Tuple[int, CallResult]:
        """Estimate age from a face image with typed configuration.

        Args:
            image: Input face image
            config: Typed operation configuration

        Returns:
            Tuple of (operation_id, typed_result)
            - operation_id: Positive on success, negative on error
            - typed_result: CallResult with age estimation data

        """
        config.input_image_format = image.image_format
        config_bytes = Session._encoder.encode(config)
        op_id, result_json = self._session_native._estimate_age(image.image_data, image.width, image.height,
                                                                config_bytes)
        result = Session._result_decoder.decode(result_json.encode('utf-8'))
        return op_id, result

    def face_iso(
            self,
            image: ImageInputArg,
            config: OperationConfig
    ) -> Tuple[int, CallResult, bytes]:
        """Process face image according to ISO standards with typed configuration.

        Args:
            image: Input face image
            config: Typed operation configuration

        Returns:
            Tuple of (operation_id, typed_result, iso_image_bytes)
            - operation_id: Positive on success, negative on error
            - typed_result: CallResult with ISO processing metadata
            - iso_image_bytes: Raw bytes of ISO-compliant face image

        """
        config.input_image_format = image.image_format
        config_bytes = Session._encoder.encode(config)
        op_id, result_json, iso_image = self._session_native._face_iso(image.image_data, image.width, image.height,
                                                                       config_bytes)
        result = Session._result_decoder.decode(result_json.encode('utf-8'))
        return op_id, result, iso_image

    def anti_spoofing(
            self,
            image: ImageInputArg,
            config: OperationConfig
    ) -> tuple[int, CallResult]:
        """Perform anti-spoofing detection on a face image with typed configuration.

        Args:
            image: Input face image
            config: Typed operation configuration

        Returns:
            Tuple of (operation_id, typed_result)
            - operation_id: Positive on success, negative on error
            - typed_result: CallResult with age estimation data

        """
        config.input_image_format = image.image_format
        config_bytes = Session._encoder.encode(config)

        op_id, result_json = self._session_native._anti_spoofing(image.image_data, image.width, image.height,
                                                                 config_bytes)
        result = Session._result_decoder.decode(result_json.encode('utf-8'))
        return op_id, result

    def doc_scan_face(
            self,
            image: ImageInputArg,
            config: OperationConfig
    ) -> Tuple[int, CallResult, bytes, bytes]:
        """Scan document and extract face with typed configuration.

        Args:
            image: Input document image
            config: Typed operation configuration

        Returns:
            Tuple of (operation_id, doc_image, face_image, typed_result)
            - operation_id: Positive on success, negative on error
            - typed_result: CallResult with document and face metadata
            - doc_image: Cropped document image bytes
            - face_image: Cropped face from document bytes


        """
        config.input_image_format = image.image_format
        config_bytes = Session._encoder.encode(config)
        op_id, result_json, doc_image, face_image,  = self._session_native._doc_scan_face(
            config_bytes, image.image_data, image.width, image.height
        )
        result = Session._result_decoder.decode(result_json.encode('utf-8'))
        return op_id, result, doc_image, face_image

    def user_delete(
            self,
            puid: str,
            config: OperationConfig
    ) -> Tuple[int, CallResult]:
        """Delete a user by PUID with typed configuration.

        Args:
            puid: User's unique identifier to delete
            config: Typed operation configuration

        Returns:
            Tuple of (operation_id, typed_result)
            - operation_id: Positive on success, negative on error
            - typed_result: CallResult with deletion status

        """
        config_bytes = Session._encoder.encode(config)
        op_id, result_json = self._session_native._user_delete(config_bytes, puid.encode('utf-8'))
        result = Session._result_decoder.decode(result_json.encode('utf-8'))
        return op_id, result

    def __del__(self):
        """Cleanup when session is destroyed."""
        if self._session_native is not None:
            del self._session_native
            self._session_native = None

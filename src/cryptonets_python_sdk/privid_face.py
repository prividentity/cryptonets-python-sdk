from ctypes import *
from typing import Optional

from cryptonets_python_sdk.img_utils import ImageUtils
from cryptonets_python_sdk.library_loader import LibraryLoadStrategy, DefaultLibraryLoadStrategy, LibraryLoadError,SystemInfoUtility


class ImageInputArg:
    image_format: str
    image_data: bytes
    width: int
    height: int
    orientation: int

    def __init__(self, image_in, image_format: str,apply_rotation: bool = True):
        ImageUtils.check_image_format(image_format)
        self.image_array = None
        if isinstance(image_in, str):
            self.image_array,self.image_format = ImageUtils.image_path_to_numpy_array(image_in, image_format,apply_rotation)
            ImageUtils.check_image_array(self.image_array, self.image_format)
            self.width = self.image_array.shape[1]
            self.height = self.image_array.shape[0]
            self.image_data = self.image_array.tobytes()
            self.orientation = 1
        elif isinstance(image_in, np.ndarray):
            self.image_array = image_in
            if image_format == '':
                raise ArgumentError("Image format should not be empty when using numpy array")
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

class PrivIDError(Exception):
    """Base exception for PrivID errors"""
    pass

class SessionError(PrivIDError):
    """Exception for session-related errors"""
    pass

class Session:
    """A session for face recognition operations
    """
    
    def __init__(self,settings: str):
        """Initialize a session
        
        Args:
            settings: Session settings as JSON string
        Note:
            This constructor is intended for internal use only.
            External code should use PrivIDFaceLib.create_session()
        """
        if not PrivIDFaceLib.is_initialized():
            raise SessionError("PrivIDFaceLib is not initialized. Call PrivIDFaceLib.initialize() first.")
        self._lib = PrivIDFaceLib._lib
        self._ffibuilder = PrivIDFaceLib._ffibuilder
        self._session = None
        
        # Convert settings string to bytes
        settings_bytes = settings.encode('utf-8')
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
     
            
    def set_configuration(self, config: str) -> bool:
        """Set custom configuration for the session"""
        config_bytes = config.encode('utf-8')
        return self._lib.privid_set_configuration(self._session, config_bytes, len(config_bytes))

    def _validate(self, image_bytes: bytes, image_width: int, image_height: int, user_config: str = "") -> tuple[int, str]:
        """Internal method to validate a face image"""
        config_bytes = user_config.encode('utf-8')
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_validate(
            self._session, image_bytes, image_width, image_height,
            config_bytes, len(config_bytes), result_ptr, result_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        self._lib.privid_free_char_buffer(result_ptr[0])
        return op_id, result

    def validate(self, image_input: ImageInputArg, user_config: str = "") -> tuple[int, str]:
        """Validate a face image using ImageInputArg"""
        return self._validate(image_input.image_data, image_input.width, image_input.height, user_config)

    def _face_iso(self, image_bytes: bytes, width: int, height: int, user_config: str = "") -> tuple[int, str, bytes]:
        """Internal method to process face image according to ISO standards"""
        config_bytes = user_config.encode('utf-8')
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')
        iso_image_ptr = self._ffibuilder.new('uint8_t **')
        iso_image_len = self._ffibuilder.new('int *')

        # API signature: privid_face_iso(session_ptr, image_bytes, width, height,
        #                                 user_config, user_config_length,
        #                                 result_out, result_out_length,
        #                                 output_iso_image_bytes, output_iso_image_bytes_length)
        op_id = self._lib.privid_face_iso(
            self._session, image_bytes, width, height,
            config_bytes, len(config_bytes),
            result_ptr, result_len,
            iso_image_ptr, iso_image_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        iso_image = self._ffibuilder.buffer(iso_image_ptr[0], iso_image_len[0])

        self._lib.privid_free_char_buffer(result_ptr[0])
        self._lib.privid_free_buffer(iso_image_ptr[0])

        return op_id, result, bytes(iso_image)

    def face_iso(self, image_input: ImageInputArg, user_config: str = "") -> tuple[int, str, bytes]:
        """Process face image according to ISO standards using ImageInputArg"""
        return self._face_iso(image_input.image_data, image_input.width, image_input.height, user_config)
    
    def _anti_spoofing(self, image_bytes: bytes, width: int, height: int, user_config: str = "") -> tuple[int, str]:
        """Internal method for anti-spoofing detection on a face image"""
        config_bytes = user_config.encode('utf-8')
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')
        
        op_id = self._lib.privid_anti_spoofing(
            self._session, image_bytes, width, height,
            config_bytes, len(config_bytes),
            result_ptr, result_len
        )
        
        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        self._lib.privid_free_char_buffer(result_ptr[0])
        return op_id, result

    def anti_spoofing(self, image_input: ImageInputArg, user_config: str = "") -> tuple[int, str]:
        """Perform anti-spoofing detection on a face image using ImageInputArg"""
        return self._anti_spoofing(image_input.image_data, image_input.width, image_input.height, user_config)
    
    def _face_compare_files(self, fudge_factor: float, user_config: str,
                           image_a: bytes, image_a_width: int, image_a_height: int,
                           image_b: bytes, image_b_width: int, image_b_height: int) -> tuple[int, str]:
        """Internal method to compare two face images with a fudge factor"""
        config_bytes = user_config.encode('utf-8')
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_face_compare_files(
            self._session, fudge_factor,
            config_bytes, len(config_bytes),
            image_a, len(image_a), image_a_width, image_a_height,
            image_b, len(image_b), image_b_width, image_b_height,
            result_ptr, result_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        self._lib.privid_free_char_buffer(result_ptr[0])

        return op_id, result

    def face_compare_files(self, fudge_factor: float, user_config: str,
                          image_a: ImageInputArg, image_b: ImageInputArg) -> tuple[int, str]:
        """Compare two face images with a fudge factor using ImageInputArg

        Args:
            fudge_factor: Comparison tolerance/threshold factor
            user_config: JSON configuration string
            image_a: First face image to compare
            image_b: Second face image to compare

        Returns:
            tuple[int, str]: Status code and JSON result containing comparison data
        """
        return self._face_compare_files(
            fudge_factor, user_config,
            image_a.image_data, image_a.width, image_a.height,
            image_b.image_data, image_b.width, image_b.height
        )

    def _doc_scan_face(self, user_config: str, image: bytes, width: int, height: int) -> tuple[int, bytes, bytes, str]:
        """Internal method to scan a document for face and extract it"""
        config_bytes = user_config.encode('utf-8')
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')
        doc_ptr = self._ffibuilder.new('uint8_t **')
        doc_len = self._ffibuilder.new('int *')
        face_ptr = self._ffibuilder.new('uint8_t **')
        face_len = self._ffibuilder.new('int *')
        
        op_id = self._lib.privid_doc_scan_face(
            self._session, config_bytes, len(config_bytes),
            image, width, height,
            doc_ptr, doc_len,
            face_ptr, face_len,
            result_ptr, result_len
        )
        
        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        doc = self._ffibuilder.buffer(doc_ptr[0], doc_len[0])
        face = self._ffibuilder.buffer(face_ptr[0], face_len[0])
        
        self._lib.privid_free_char_buffer(result_ptr[0])
        self._lib.privid_free_buffer(doc_ptr[0])
        self._lib.privid_free_buffer(face_ptr[0])

        return op_id, bytes(doc), bytes(face), result

    def doc_scan_face(self, user_config: str, image: ImageInputArg) -> tuple[int, bytes, bytes, str]:
        """Scan a document for face and extract it using ImageInputArg"""
        return self._doc_scan_face(user_config, image.image_data, image.width, image.height)
    
    def _estimate_age(self, image_bytes: bytes, width: int, height: int, user_config: str = "") -> tuple[int, str]:
        """Internal method to estimate age from a face image"""
        config_bytes = user_config.encode('utf-8')
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_estimate_age(
            self._session, image_bytes, width, height,
            config_bytes, len(config_bytes),
            result_ptr, result_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        self._lib.privid_free_char_buffer(result_ptr[0])
        return op_id, result

    def estimate_age(self, image_input: ImageInputArg, user_config: str = "") -> tuple[int, str]:
        """Estimate age from a face image using ImageInputArg"""
        return self._estimate_age(image_input.image_data, image_input.width, image_input.height, user_config)

    def _estimate_age_with_stdd(self, image_bytes: bytes, width: int, height: int, user_config: str = "") -> tuple[int, str]:
        """Internal method to estimate age with standard deviation from a face image"""
        config_bytes = user_config.encode('utf-8')
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_estimate_age_with_stdd(
            self._session, image_bytes, width, height,
            config_bytes, len(config_bytes),
            result_ptr, result_len
        )

        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        self._lib.privid_free_char_buffer(result_ptr[0])
        return op_id, result

    def estimate_age_with_stdd(self, image_input: ImageInputArg, user_config: str = "") -> tuple[int, str]:
        """Estimate age with standard deviation from a face image using ImageInputArg

        This method provides age estimation along with standard deviation metrics.

        Args:
            image_input: ImageInputArg containing the face image
            user_config: Optional JSON configuration string

        Returns:
            tuple[int, str]: Status code and JSON result containing age and standard deviation
        """
        return self._estimate_age_with_stdd(image_input.image_data, image_input.width, image_input.height, user_config)
    
    def _enroll_onefa(self, user_config: str, images: bytes,
                     image_width: int, image_height: int) -> tuple[int, str]:
        """Internal method to enroll one or more face images

        Note: The new API signature no longer returns best_input image or requires image_count.
        """
        config_bytes = user_config.encode('utf-8')
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_enroll_onefa(
            self._session,
            config_bytes, len(config_bytes),
            images,
            image_width, image_height,
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
        return self._enroll_onefa(user_config, image_input.image_data, image_input.width, image_input.height)
    
    def _face_predict_onefa(self, user_config: str, images: bytes, image_size: int,
                          image_width: int, image_height: int) -> tuple[int, str]:
        """Internal method to predict using enrolled face images"""
        config_bytes = user_config.encode('utf-8')
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')

        op_id = self._lib.privid_face_predict_onefa(
            self._session,
            config_bytes, len(config_bytes),
            images, image_size,
            image_width, image_height,
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
        image_data = image_input.image_data
        return self._face_predict_onefa(user_config, image_data, len(image_data), image_input.width, image_input.height)
    
    def user_delete(self, user_config: str, puid: str) -> tuple[int, str]:
        """Delete a user by PUID"""
        config_bytes = user_config.encode('utf-8')
        puid_bytes = puid.encode('utf-8')
        result_ptr = self._ffibuilder.new('char **')
        result_len = self._ffibuilder.new('int *')
        
        op_id = self._lib.privid_user_delete(
            self._session, config_bytes, len(config_bytes),
            puid_bytes, len(puid_bytes),
            result_ptr, result_len
        )
        
        result = self._ffibuilder.string(result_ptr[0], result_len[0]).decode('utf-8')
        self._lib.privid_free_char_buffer(result_ptr[0])
        return op_id, result

import threading

class PrivIDFaceLib:
    """Main interface to the PrivID Face Recognition library (static, thread-safe)"""

    _lib = None
    _ffibuilder = None
    _models_cache_directory = None
    _initialized = False
    _lock = threading.RLock()  # Use a reentrant lock for thread safety

    @classmethod
    def initialize(cls, load_strategy: Optional[LibraryLoadStrategy] = None, log_level: int = 0):
        """Initialize the PrivID Face library.

        Args:
            load_strategy: Optional custom library loading strategy
            log_level: Logging level (0=off, 1=error, 2=warning, 3=info, 4=debug)

        Raises:
            LibraryLoadError: If library loading or initialization fails
        """
        with cls._lock:
            if cls._initialized:
                return
            if load_strategy is None:
                load_strategy = DefaultLibraryLoadStrategy()
            try:
                cls._lib, cls._ffibuilder = load_strategy.load_library()
                cls._models_cache_directory = SystemInfoUtility.get_models_cache_directory(LibraryLoadStrategy.PACKAGE_NAME)
                cls._initialize_lib(cls._models_cache_directory, log_level)
                # spin till initialized
                import time
                for _ in range(100):
                    if cls.is_library_initialized():
                        break
                    time.sleep(0.1)
                if not cls.is_library_initialized():
                    cls._initialized = False    
                cls._initialized = True
            except Exception as e:
                cls._lib = None
                cls._ffibuilder = None
                cls._initialized = False
                raise LibraryLoadError(f"Failed to load library: {str(e)}")

    @classmethod
    def _initialize_lib(cls, models_directory: str, log_level: int = 0):
        """Internal method to initialize the native library.

        Args:
            models_directory: Path to models cache directory
            log_level: Logging level
        """
        dir_bytes = models_directory.encode('utf-8')
        cls._lib.privid_initialize_lib(dir_bytes, len(dir_bytes), log_level)

    @classmethod
    def shutdown(cls):
        """Shutdown the library and release all resources.

        This should be called when you're completely done with the library.
        After calling this, you must call initialize() again before using the library.
        """
        with cls._lock:
            if cls._initialized and cls._lib:
                cls._lib.privid_shutdown_lib()
                cls._lib = None
                cls._ffibuilder = None
                cls._models_cache_directory = None
                cls._initialized = False

    @classmethod
    def get_version(cls) -> str:
        """Get the library version string.

        Returns:
            str: Version string of the native library
        """
        cls._ensure_initialized()
        version_ptr = cls._lib.privid_get_version()
        version = cls._ffibuilder.string(version_ptr).decode('utf-8')
        return version

    @classmethod
    def set_log_level(cls, level: int) -> bool:
        """Set the logging level for the library.

        Args:
            level: Logging level (0=off, 1=error, 2=warning, 3=info, 4=debug)

        Returns:
            bool: True if successful, False otherwise
        """
        cls._ensure_initialized()
        return cls._lib.privid_set_log_level(level)

    @classmethod
    def get_log_level(cls) -> int:
        """Get the current logging level.

        Returns:
            int: Current logging level
        """
        cls._ensure_initialized()
        return cls._lib.privid_get_log_level()

    @classmethod
    def get_models_cache_directory(cls) -> str:
        """Get the models cache directory path.

        This returns the directory where models and native libraries are cached.

        Returns:
            str: Path to the models cache directory
        """
        cls._ensure_initialized()
        return cls._models_cache_directory

    @classmethod
    def get_models_cache_directory_from_lib(cls) -> str:
        """Get the models cache directory from the native library.

        Returns:
            str: Path to the models cache directory as reported by the native library
        """
        cls._ensure_initialized()
        dir_ptr = cls._ffibuilder.new('char **')
        dir_len = cls._ffibuilder.new('int *')

        if cls._lib.privid_get_models_cache_directory(dir_ptr, dir_len):
            result = cls._ffibuilder.string(dir_ptr[0], dir_len[0]).decode('utf-8')
            cls._lib.privid_free_char_buffer(dir_ptr[0])
            return result
        return ""

    @classmethod
    def is_library_initialized(cls) -> bool:
        """Check if the native library is initialized.

        This checks the native library's internal initialization state.

        Returns:
            bool: True if the native library is initialized, False otherwise
        """
        if cls._lib is None:
            return False
        return cls._lib.privid_is_library_initialized()

    @classmethod
    def free_buffer(cls, buffer_ptr):
        """Free a buffer allocated by the native library.

        This should be used to free buffers returned by native library functions.
        Note: Most SDK methods already handle buffer cleanup automatically.

        Args:
            buffer_ptr: Pointer to the buffer to free (CFFI pointer object)

        Warning:
            Only use this if you're directly calling native library functions.
            Using this on already-freed buffers will cause undefined behavior.
        """
        cls._ensure_initialized()
        if buffer_ptr:
            cls._lib.privid_free_buffer(buffer_ptr)

    @classmethod
    def free_char_buffer(cls, buffer_ptr):
        """Free a character buffer allocated by the native library.

        This should be used to free character buffers returned by native library functions.
        Note: Most SDK methods already handle buffer cleanup automatically.

        Args:
            buffer_ptr: Pointer to the character buffer to free (CFFI pointer object)

        Warning:
            Only use this if you're directly calling native library functions.
            Using this on already-freed buffers will cause undefined behavior.
        """
        cls._ensure_initialized()
        if buffer_ptr:
            cls._lib.privid_free_char_buffer(buffer_ptr)

    @classmethod
    def _ensure_initialized(cls):
        """Ensure the library is initialized, initializing if necessary."""
        if not cls._initialized:
            cls.initialize()

    @classmethod
    def is_initialized(cls) -> bool:
        """Check if the PrivIDFaceLib wrapper is initialized.

        Returns:
            bool: True if initialized, False otherwise
        """
        with cls._lock:
            return cls._initialized
        
        

import threading
from ctypes import *
from typing import Optional
from cryptonets_python_sdk.library_loader import LibraryLoadStrategy, DefaultLibraryLoadStrategy, LibraryLoadError,SystemInfoUtility

class PrivIDError(Exception):
    """Base exception for PrivID errors"""
    pass

class PrivIDFaceLib:
    """Main interface to the PrivID Face Recognition library (static, thread-safe)"""

    _lib = None
    _ffibuilder = None
    _models_cache_directory = None
    _initialized = False
    _lock = threading.RLock()  # Use a reentrant lock for thread safety
    _native_sdk_version = None

    @classmethod
    def initialize(cls, load_strategy: Optional[LibraryLoadStrategy] = None, log_level: int = 0):
        """Initialize the PrivID Face library.

        Args:
            load_strategy: Optional custom library loading strategy
            log_level: Logging level (0=error, 1=warn, 2=info, 3=debug)

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
                dir_bytes = cls._models_cache_directory.encode('utf-8')
                cls._lib.privid_initialize_lib(dir_bytes, len(dir_bytes), log_level)
                # spin till initialized
                import time
                for _ in range(100):
                    if cls._lib.privid_is_library_initialized():
                        break
                    time.sleep(0.1)
                version_ptr = cls._lib.privid_get_version()
                cls._native_sdk_version = cls._ffibuilder.string(version_ptr).decode('utf-8')
                if not cls._lib.privid_is_library_initialized():
                    cls._initialized = False    
                cls._initialized = True
            except Exception as e:
                cls._lib = None
                cls._ffibuilder = None
                cls._initialized = False
                raise LibraryLoadError(f"Failed to load library: {str(e)}")

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
                cls._native_sdk_version = None
                cls._ffibuilder = None
                cls._models_cache_directory = None
                cls._initialized = False

    @classmethod
    def get_native_sdk_version(cls) -> str:
        """Get the library version string.

        Returns:
            str: Version string of the native library
        """
        cls._throw_if_not_initialized()
        return cls._native_sdk_version

    @classmethod
    def set_log_level(cls, level: int) -> bool:
        """Set the logging level for the library.

        Args:
            level: Logging level (0=error, 1=warn, 2=info, 3=debug)

        Returns:
            bool: True if successful, False otherwise
        """
        cls._throw_if_not_initialized()
        return cls._lib.privid_set_log_level(level)

    @classmethod
    def get_log_level(cls) -> int:
        """Get the current logging level.

        Returns:
            int: Current logging level
        """
        cls._throw_if_not_initialized()
        return cls._lib.privid_get_log_level()

    @classmethod
    def get_models_cache_directory(cls) -> str:
        """Get the models cache directory path.

        This returns the directory where models and native libraries are cached.

        Returns:
            str: Path to the models cache directory
        """
        cls._throw_if_not_initialized()
        return cls._models_cache_directory

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
        cls._throw_if_not_initialized()
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
        cls._throw_if_not_initialized()
        if buffer_ptr:
            cls._lib.privid_free_char_buffer(buffer_ptr)

    @classmethod
    def is_initialized(cls) -> bool:
        """Check if the PrivIDFaceLib wrapper is initialized.
        Thread safe.
        Returns:
            bool: True if initialized, False otherwise
        """
        with cls._lock:
            return cls._initialized

    @classmethod
    def _throw_if_not_initialized(cls):
        with cls._lock:
            if not cls._initialized:
                raise PrivIDError("Library not initialized")

    @classmethod
    def _get_models_cache_directory_from_lib(cls) -> str:
        """Not used : Gets the models cache directory from the native library.

        Returns:
            str: Path to the models cache directory as reported by the native library
        """
        cls._throw_if_not_initialized()
        dir_ptr = cls._ffibuilder.new('char **')
        dir_len = cls._ffibuilder.new('int *')

        if cls._lib.privid_get_models_cache_directory(dir_ptr, dir_len):
            result = cls._ffibuilder.string(dir_ptr[0], dir_len[0]).decode('utf-8')
            cls._lib.privid_free_char_buffer(dir_ptr[0])
            return result
        return ""

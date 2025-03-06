import gc
import memory_profiler
import pytest
import time
import weakref

from cryptonets_python_sdk.factor import FaceFactor, Singleton
from cryptonets_python_sdk.handler.nativeMethods import NativeMethods
from cryptonets_python_sdk.settings.loggingLevel import LoggingLevel
from cryptonets_python_sdk.settings.cacheType import CacheType

def measure_memory_usage(func, *args, **kwargs):
    """Measure memory usage for a given function."""
    mem_before = memory_profiler.memory_usage()[0]
    func(*args, **kwargs)
    mem_after = memory_profiler.memory_usage()[0]
    return mem_after - mem_before

@pytest.fixture(scope="function")
def face_factor():
    face_factor_instance = FaceFactor(api_key="X", server_url="X")
    yield face_factor_instance


@pytest.mark.memory_profile
def test_memory_leaks_enroll(face_factor):
    """Test for memory leaks during enroll operation."""
    
    def allocate_memory_enroll():
        time.sleep(1)
        for i in range(20):
            enroll_handle = face_factor.enroll(image_data="./example/test_images/18.jpg")
        assert i == 19
    
    mem_increase = measure_memory_usage(allocate_memory_enroll)
    
    # Assert memory increase is below the threshold
    assert mem_increase < 5, f"Memory increased by more than 150 MB (increased {mem_increase} MB)"


@pytest.mark.memory_profile
def test_memory_leaks_delete(face_factor):
    """Test for memory leaks during delete operation."""
    
    def allocate_memory_delete():
        time.sleep(1)
        for i in range(20):
            delete_handle = face_factor.delete(puid="X")
        assert i == 19
    
    mem_increase = measure_memory_usage(allocate_memory_delete)
    
    # Assert memory increase is below the threshold
    assert mem_increase < 150, f"Memory increased by more than 150 MB (increased {mem_increase} MB)"


def test_face_factor_garbage_collection():
    """Test if FaceFactor is being garbage collected correctly."""

    face_factor_instance = FaceFactor(api_key="X", server_url="X")
    
    # Create a weak reference to the FaceFactor instance
    weak_ref = weakref.ref(face_factor_instance, lambda ref: print("FaceFactor is being garbage collected"))
    
    # At this point, the weak reference is still alive
    assert weak_ref() is face_factor_instance, "Weak reference should point to the instance."
    
    # Delete the instance to trigger garbage collection
    print("Singleton instances: ", Singleton._instances)
    # Singleton._instances.clear()
    del face_factor_instance

    print(f"INSTANCES AFTER DELETE = {FaceFactor._instances}")

    
    # Optionally, manually trigger garbage collection before checking weak reference
    gc.collect()  # Force garbage collection
    print("Manually triggered garbage collection.")
    
    # At this point, the weak reference should be None, as the object should be collected
    assert weak_ref() is None, "FaceFactor should have been garbage collected after gc.collect()"


def test_singleton_instance_creation():
    """Test if only one instance of FaceFactor is created."""
    instance1 = FaceFactor("X", "X")
    instance2 = FaceFactor("Y", "Y")  # Should return the same instance as instance1

    assert instance1 is instance2, "Singleton instances should be the same object"


def test_singleton_cleanup():
    """Test if the singleton instance is properly cleaned up on deletion."""
    
    # Create instance
    instance = FaceFactor("X", "X")
    
    # Create a weak reference to track garbage collection
    weak_ref = weakref.ref(instance)
    
    # Ensure weak reference is still valid
    assert weak_ref() is instance, "Weak reference should initially point to the instance."
    
    # Delete the instance
    del instance
    
    # Force garbage collection
    gc.collect()
    
    # Ensure weak reference is now None (garbage collected)
    assert weak_ref() is None, "FaceFactor instance should have been garbage collected."
    
    # Ensure the singleton registry is empty
    assert FaceFactor not in Singleton._instances, "Instance should be removed from the singleton registry."

def test_singleton_registry():
    """Test that the singleton registry correctly stores and removes instances."""
    
    instance = FaceFactor("Z", "Z")
    
    assert FaceFactor in Singleton._instances, "FaceFactor should be in the singleton registry."
    
    del instance

    gc.collect()  # Force cleanup

    assert FaceFactor not in Singleton._instances, "FaceFactor should be removed from the singleton registry after deletion."

@pytest.mark.memory_profile
def test_memory_leaks_is_valid(face_factor):
    """Test for memory leaks during is_valid operation."""
    
    def allocate_memory_is_valid():
        time.sleep(1)
        for i in range(150):
            is_valid_handle = face_factor.is_valid(image_data="./example/test_images/18.jpg")
        assert i == 149
    
    mem_increase = measure_memory_usage(allocate_memory_is_valid)
    
    # Assert memory increase is below the threshold
    assert mem_increase < 20, f"Memory increased by more than 20 MB (increased {mem_increase} MB)"



# @pytest.mark.memory_profile
# def test_memory_leaks_native_methods(face_factor):
#     """Test for memory leaks from NativeMethods class."""
    
#     def allocate_memory_native_methods():
#         time.sleep(1)
#         for i in range(150):
#             native_handle = NativeMethods(
#                 api_key="00000000000000001962",
#                 server_url="http://localhost:99999",
#                 local_storage_path="/tmp",
#                 tf_num_thread=0,
#                 logging_level=LoggingLevel.off,
#                 cache_type=CacheType.OFF
#             )
#             native_handle._load_linux_libraries()
#             del native_handle
#         time.sleep(2)
#         assert i == 149
    
#     mem_increase = measure_memory_usage(allocate_memory_native_methods)
    
#     # Assert memory increase is below the threshold
#     assert mem_increase < 10, f"Memory increased by more than 10 MB (increased {mem_increase} MB)"



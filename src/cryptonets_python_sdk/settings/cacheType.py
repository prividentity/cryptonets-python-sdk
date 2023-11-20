from enum import Enum


class CacheType(str, Enum):
    """
    Cache Type defines whether you want to store the data offline

    off - No cache

    on - Cache set in the local storage path

    """

    ON = "basic"
    OFF = "nocache"

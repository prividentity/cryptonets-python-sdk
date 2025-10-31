"""Bitwise flag utility for face and document traits.

This module provides utility functions for working with Flag enum types,
enabling extraction and inspection of bitwise flag values.
"""

from enum import Flag, IntFlag
from typing import List, TypeVar, Type, Union


# Generic type variable for Flag subclasses
FlagT = TypeVar('FlagT', bound=Union[Flag, IntFlag])


class FlagUtil:
    """Utility class for working with Flag enum types.

    This class provides static methods for extracting and checking flags
    without requiring inheritance from the flag enum types.

    Example:
        >>> from cryptonets_python_sdk.flags import FlagUtil
        >>> from cryptonets_python_sdk import FaceTraitsFlags
        >>>
        >>> # Extract active flags from integer value
        >>> active = FlagUtil.get_active_flags(FaceTraitsFlags, 5)
        >>> print(active)  # [<FaceTraitsFlags.FT_FACE_TOO_CLOSE: 1>, <FaceTraitsFlags.FT_FACE_RIGHT: 4>]
        >>>
        >>> # Get flag names
        >>> names = FlagUtil.get_flag_names(FaceTraitsFlags, 5)
        >>> print(names)  # ['FT_FACE_TOO_CLOSE', 'FT_FACE_RIGHT']
        >>>
        >>> # Check if specific flags are present
        >>> flags = FaceTraitsFlags(5)
        >>> has_close = FlagUtil.has_flag(flags, FaceTraitsFlags.FT_FACE_TOO_CLOSE)
        >>> print(has_close)  # True
        >>>
        >>> # Check if any of multiple flags are present
        >>> has_any = FlagUtil.has_any(flags, FaceTraitsFlags.FT_FACE_LEFT, FaceTraitsFlags.FT_FACE_RIGHT)
        >>> print(has_any)  # True (because FT_FACE_RIGHT is present)
        >>>
        >>> # Check if all of multiple flags are present
        >>> has_all = FlagUtil.has_all(flags, FaceTraitsFlags.FT_FACE_TOO_CLOSE, FaceTraitsFlags.FT_FACE_RIGHT)
        >>> print(has_all)  # True
    """

    @staticmethod
    def get_active_flags(flag_type: Type[FlagT], value: int) -> List[FlagT]:
        """Extract all active individual flags from an integer value.

        Args:
            flag_type: The Flag or IntFlag enum class
            value: Integer value representing combined flags

        Returns:
            List of individual flags that are set in the value,
            excluding zero-value flags.

        Example:
            >>> from cryptonets_python_sdk import FaceTraitsFlags
            >>> active = FlagUtil.get_active_flags(FaceTraitsFlags, 5)
            >>> active
            [<FaceTraitsFlags.FT_FACE_TOO_CLOSE: 1>, <FaceTraitsFlags.FT_FACE_RIGHT: 4>]
            >>> for flag in active:
            ...     print(f"{flag.name}: {flag.value}")
            FT_FACE_TOO_CLOSE: 1
            FT_FACE_RIGHT: 4
        """
        flags_instance = flag_type(value)
        active = []
        for flag in flag_type:
            # Skip zero-value flags and only include flags that are set
            if flag.value != 0 and flag in flags_instance:
                active.append(flag)
        return active

    @staticmethod
    def get_flag_names(flag_type: Type[FlagT], value: int) -> List[str]:
        """Extract names of all active flags from an integer value.

        Args:
            flag_type: The Flag or IntFlag enum class
            value: Integer value representing combined flags

        Returns:
            List of flag names as strings, excluding zero-value flags.

        Example:
            >>> from cryptonets_python_sdk import FaceTraitsFlags
            >>> names = FlagUtil.get_flag_names(FaceTraitsFlags, 65)
            >>> names
            ['FT_FACE_TOO_CLOSE', 'FT_IMAGE_BLURR']
        """
        return [flag.name for flag in FlagUtil.get_active_flags(flag_type, value)]

    @staticmethod
    def has_flag(flags_instance: FlagT, flag: FlagT) -> bool:
        """Check if a specific flag is present in a flags instance.

        Args:
            flags_instance: The flag instance to check
            flag: The specific flag to check for

        Returns:
            True if the flag is present, False otherwise

        Example:
            >>> from cryptonets_python_sdk import FaceTraitsFlags
            >>> flags = FaceTraitsFlags(5)
            >>> FlagUtil.has_flag(flags, FaceTraitsFlags.FT_FACE_TOO_CLOSE)
            True
            >>> FlagUtil.has_flag(flags, FaceTraitsFlags.FT_FACE_LEFT)
            False
        """
        return flag in flags_instance

    @staticmethod
    def has_any(flags_instance: FlagT, *flags: FlagT) -> bool:
        """Check if any of the specified flags are present.

        Args:
            flags_instance: The flag instance to check
            *flags: Variable number of flags to check

        Returns:
            True if any of the specified flags are present, False otherwise

        Example:
            >>> from cryptonets_python_sdk import FaceTraitsFlags
            >>> flags = FaceTraitsFlags.FT_FACE_TOO_CLOSE | FaceTraitsFlags.FT_IMAGE_BLURR
            >>> FlagUtil.has_any(flags, FaceTraitsFlags.FT_FACE_LEFT, FaceTraitsFlags.FT_IMAGE_BLURR)
            True
            >>> FlagUtil.has_any(flags, FaceTraitsFlags.FT_FACE_LEFT, FaceTraitsFlags.FT_FACE_UP)
            False
        """
        for flag in flags:
            if flag in flags_instance:
                return True
        return False

    @staticmethod
    def has_all(flags_instance: FlagT, *flags: FlagT) -> bool:
        """Check if all of the specified flags are present.

        Args:
            flags_instance: The flag instance to check
            *flags: Variable number of flags to check

        Returns:
            True if all specified flags are present, False otherwise

        Example:
            >>> from cryptonets_python_sdk import FaceTraitsFlags
            >>> flags = FaceTraitsFlags.FT_FACE_TOO_CLOSE | FaceTraitsFlags.FT_IMAGE_BLURR
            >>> FlagUtil.has_all(flags, FaceTraitsFlags.FT_FACE_TOO_CLOSE, FaceTraitsFlags.FT_IMAGE_BLURR)
            True
            >>> FlagUtil.has_all(flags, FaceTraitsFlags.FT_FACE_TOO_CLOSE, FaceTraitsFlags.FT_FACE_LEFT)
            False
        """
        for flag in flags:
            if flag not in flags_instance:
                return False
        return True

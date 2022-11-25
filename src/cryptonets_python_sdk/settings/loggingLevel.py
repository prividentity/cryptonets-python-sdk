from enum import Enum


class LoggingLevel(Enum):
    # Logging is completely disabled.
    off = 0
    # Only minimal logging is enabled.
    minimal = 1
    # The normal logging level.
    normal = 2
    # Full logging is enabled.
    full = 3

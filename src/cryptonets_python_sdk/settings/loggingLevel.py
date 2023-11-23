from enum import Enum


class LoggingLevel(Enum):
    """
    LoggingLevel on how much debug data has to be displayed

    off - No logs

    minimal - Important logs on operation

    normal - Default log

    full - Complete logs

    """

    off = 0
    minimal = 1
    normal = 2
    full = 3

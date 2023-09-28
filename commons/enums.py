from enum import Enum


class IndicatorEnum(Enum):
    NULL = "null"
    SAME = "same"
    UP = "up"
    DOWN = "down"


class TimeFrame(Enum):
    LONG_TERM = "long_term"
    MEDIUM_TERM = "medium_term"
    SHORT_TERM = "short_term"

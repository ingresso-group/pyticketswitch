from enum import Enum


MONTH_NUMBERS = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7,
    'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12,
}


class DiscountSemanticType(Enum):
    BLUELIGHT = "bluelight"
    CARER = "carer"
    CHILD = "child"
    DISABLED = "disabled"
    INFANT = "infant"
    MILITARY = "military"
    SENIOR = "senior"
    STUDENT = "student"
    UNWAGED = "unwaged"
    YOUTH = "youth"
    STANDARD = "standard"

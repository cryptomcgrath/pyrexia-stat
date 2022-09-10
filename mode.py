from enum import Enum

class Mode(Enum):
    HEAT = "heat"
    COOL = "cool"
    NONE = "none"

    def from_string(s):
        for m in Mode:
            if m.name == s:
                return m
        return Mode['NONE']


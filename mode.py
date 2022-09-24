from enum import Enum

class Mode(Enum):
    HEAT = "heat"
    COOL = "cool"
    NONE = "none"

    def from_string(s):
        if s == "heat":
            return Mode.HEAT
        if s == "cool":
            return Mode.COOL
        return Mode['NONE']


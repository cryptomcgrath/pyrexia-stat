from enum import Enum

class Mode(Enum):
    HEAT = "heat"
    COOL = "cool"
    NONE = "none"

    def from_string(s):
        if s == "heat" or s == "HEAT":
            return Mode.HEAT
        if s == "cool" or s == "COOL":
            return Mode.COOL
        return Mode['NONE']


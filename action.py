from enum import Enum

class Action(Enum):
    COMMAND_OFF = "COMMAND_OFF"
    COMMAND_ON = "COMMAND_ON"
    WAIT_SATISFIED = "WAIT_SATISFIED"
    WAIT_CALL = "WAIT_CALL"
    WAIT_REST = "WAIT_REST"
    WAIT_MIN_RUN = "WAIT_MIN_RUN"
    DISABLED = "DISABLED"

    def from_string(s):
        if s == "COMMAND_OFF":
            return Action.COMMAND_OFF
        if s == "COMMAND_ON":
            return Action.COMMAND_ON
        if s == "WAIT_SATISFIED":
            return Action.WAIT_SATISFIED
        if s == "WAIT_CALL":
            return Action.WAIT_CALL
        if s == "WAIT_REST":
            return Action.WAIT_REST
        if s == "WAIT_MIN_RUN":
            return Action.WAIT_MIN_RUN
        if s == "DISABLED":
            return Action.DISABLED
        return None 


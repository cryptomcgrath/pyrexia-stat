from enum import Enum

class Action(Enum):
    COMMAND_OFF = "COMMAND_OFF"
    COMMAND_ON = "COMMAND_ON"
    WAIT_SATISFIED = "WAIT_SATISFIED"
    WAIT_CALL = "WAIT_CALL"
    WAIT_REST = "WAIT_REST"
from enum import Enum
from pyrexia.mode import Mode
from pyrexia.action import Action

class Program:
    id = 0
    name = ""
    sensor_id = 0 
    control_id = 0
    set_point = 0
    mode = Mode['NONE']
    enabled = False
    last_action = None

    def __init__(self, id, name, sensor_id, control_id, set_point, mode, enabled, last_action):
        self.id = id
        self.name = name
        self.sensor_id = sensor_id
        self.control_id = control_id
        self.set_point = set_point
        self.mode = mode
        self.enabled = enabled
        self.last_action = last_action

    def from_dict(dict):
        name = dict["name"]
        return Program(dict["id"], dict["name"], dict["sensor_id"], dict["control_id"], dict["set_point"], Mode.from_string(dict["mode"]), dict["enabled"]==1, Action.from_string(dict["last_action"]))

    def last_action_on(self):
        return self.last_action == Action.COMMAND_ON or self.last_action == Action.WAIT_SATISFIED or self.last_action == Action.WAIT_MIN_RUN


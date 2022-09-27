from enum import Enum
from mode import Mode
from action import Action
import control
import sensor

class Program:
    id = 0
    name = ""
    sensor_id = 0 
    control_id = 0
    set_point = 0
    mode = Mode['NONE']
    enabled = False

    def __init__(self, id, name, sensor_id, control_id, set_point, mode, enabled):
        self.id = id
        self.name = name
        self.sensor_id = sensor_id
        self.control_id = control_id
        self.set_point = set_point
        self.mode = mode
        self.enabled = enabled

    def from_dict(dict):
        name = dict["name"]
        return Program(dict["id"], dict["name"], dict["sensor_id"], dict["control_id"], dict["set_point"], Mode.from_string(dict["mode"]), dict["enabled"]==1)


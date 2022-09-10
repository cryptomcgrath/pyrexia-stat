from enum import Enum
from mode import Mode
from action import Action
import control
import sensor

class Program:
    name = ""
    sensor_id = 0 
    control_id = 0
    set_point = 0
    mode = Mode['NONE']

    def __init__(self, name, sensor_id, control_id, set_point, mode):
        self.name = name
        self.sensor_id = sensor_id
        self.control_id = control_id
        self.set_point = set_point
        self.mode = mode

    def from_dict(dict):
        name = dict["name"]
        return Program(dict["name"], dict["sensor_id"], dict["control_id"], dict["set_point"], Mode.from_string(dict["mode"]))


    def get_action(controls, sensors):
        control = controls[control_id]
        sensor = sensors[sensor_id]
        
        if control.is_on():
            if is_satisfied(sensor.value, set_point, mode) and control.has_min_run(): 
                return Action["COMMAND_OFF"] 
            else:
                return Action["WAIT_SATISFIED"]

        else:
            if is_call(sensor.value, set_point, mode) and control.has_min_rest():
                return Action["COMMAND_ON"]
            else:
                return Action["WAIT_CALL"]

    def is_satisfied(sensor_value, set_point, mode):
        if mode == Mode.HEAT:
            return sensor_value > set_point

        elif mode == Mode.COOL:
            return sensor_value < set_point

        else:
            return True 

    def is_call(sensor_value, set_point, mode):
        if mode == Mode.HEAT:
            return sensor_value < set_point

        elif mode == Mode.COOL:
            return sensor.value > set_point

        else:
            return False 



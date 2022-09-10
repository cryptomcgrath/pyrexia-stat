from relay import Relay 
import utils as ut
from action import Action

class Control:
    id = 0
    name = ""
    last_off_time = 0
    last_on_time = 0
    min_rest = 0
    min_run = 0
    relay = None
    action = None

    def __init__(self, control_id, name, last_off_time, last_on_time, min_rest, min_run, gpio, gpio_on_hi):
        self.id = control_id
        self.name = name,
        self.last_off_time = last_off_time
        self.last_on_time = last_on_time
        self.min_rest = min_rest
        self.min_run = min_run
        self.relay = Relay(gpio, gpio_on_hi)


    def from_dict(dict):
        control_id = dict["id"]
        name = dict["name"]
        last_off_time = dict["last_off_time"]
        last_on_time = dict["last_on_time"]
        min_rest = dict["min_rest"]
        min_run = dict["min_run"]
        gpio = dict["gpio"]
        gpio_on_hi = dict["gpio_on_hi"]
        return Control(control_id, name, last_off_time, last_on_time, min_rest, min_run, gpio, gpio_on_hi)

    def is_on(self):
        return self.relay.is_on()

    def has_rested(self):
        return ut.currentTimeInt() - self.last_off_time > self.min_rest

    def has_min_run(self):
        return ut.currentTimeInt() - self.last_on_time > self.min_run

    def command(self, onoff):
        self.relay.command(onoff)

    def apply_action(self, program, sensors):
        program_action = self.get_action(program, sensors)

        if program_action == Action.WAIT_SATISFIED:
            action = program_action
        elif program_action == Action.COMMAND_ON:
            if action != Action.WAIT_SATISFIED:
                action = Action.COMMAND_ON
        elif program_action == Action.COMMAND_OFF:
            if action != Action.WAIT_SATISFIED and action != Action.COMMAND_ON:
                action = Action.COMMAND_OFF
        elif program_action == Action.WAIT_CALL:
            if action != Action.WAIT_SATISFIED and action != Action.COMMAND_ON and action != Action.COMMAND_OFF:
                action = Action.WAIT_CALL

    def execute_action(self):
        if self.action == Action.COMMAND_ON:
            self.command(True)
        elif self.action == Action.COMMAND_OFF:
            self.command(False)
     
    def get_action(self, program, sensors):
        sensor = next(x for x in sensors if x.id == program.sensor_id)

        if self.is_on():
            if self.is_satisfied(sensor.value, set_point, mode) and self.has_min_run():
                return Action["COMMAND_OFF"]
            else:
                return Action["WAIT_SATISFIED"]

        else:
            if self.is_call(sensor.value, set_point, mode) and self.has_min_rest():
                return Action["COMMAND_ON"]
            else:
                return Action["WAIT_CALL"]

    def is_satisfied(self, sensor_value, set_point, mode):
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


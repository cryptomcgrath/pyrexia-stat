import logging
from pyrexia.relay import Relay 
import pyrexia.utils as ut
from pyrexia.action import Action
from pyrexia.mode import Mode
import pyrexia.rest as rest

#logging.basicConfig(filename='pyrexia-debug.log', encoding='utf-8', level=logging.DEBUG)
logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger("pyrexia")

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

    def has_min_rest(self):
        return ut.currentTimeInt() - self.last_off_time > self.min_rest

    def has_min_run(self):
        return ut.currentTimeInt() - self.last_on_time > self.min_run

    def command(self, onoff):
        self.relay.command(onoff)

    def apply_action(self, program, sensors):
        program_sensor = next((x for x in sensors if x.id == program.sensor_id), None)
        if program_sensor == None:
            log.debug("program id {} could not locate sensor id {}".format(program.id, program.sensor_id))
            return None

        program_action = self.get_action(program, program_sensor)
        rest.update_program_action(program.id, program_action.name)

        if program_action == Action.WAIT_SATISFIED:
            self.action = program_action
        elif program_action == Action.COMMAND_ON:
            if self.action != Action.WAIT_SATISFIED and self.action != Action.WAIT_REST:
                self.action = Action.COMMAND_ON
        elif program_action == Action.COMMAND_OFF:
            if self.action != Action.WAIT_SATISFIED and self.action != Action.COMMAND_ON and self.action != Action.WAIT_MIN_RUN:
                self.action = Action.COMMAND_OFF
        elif program_action == Action.WAIT_CALL:
            if self.action != Action.WAIT_SATISFIED and self.action != Action.COMMAND_ON and self.action != Action.COMMAND_OFF:
                self.action = Action.WAIT_CALL
        else:
            self.action = program_action

        log.debug("program id {} program_action {} control_action {}".format(program.id, program_action.name, self.action.name)) 
        # log to history
        rest.add_history(program.id, program.set_point, program_sensor.id, program_sensor.value, self.id, self.is_on(), program_action.name, self.action.name)

    def execute_action(self):
        if self.action == Action.COMMAND_ON:
            rest.control_on(self.id)
            self.command(True)
        elif self.action == Action.COMMAND_OFF:
            rest.control_off(self.id)
            self.command(False)
        elif self.action == Action.DISABLED and self.is_on():
            rest.control_off(self.id)
            self.command(False)

    def get_action(self, program, program_sensor):
        if program.enabled == False:
            return Action.DISABLED

        if self.is_on() and program.last_action_on():
            if is_satisfied(program_sensor.value, program.set_point, program.mode):
                if self.has_min_run():
                    return Action["COMMAND_OFF"]
                else:
                    return Action["WAIT_MIN_RUN"]
            else:
                return Action["WAIT_SATISFIED"]

        elif is_call_for_on(program_sensor.value, program.set_point, program.mode):
            if self.has_min_rest():
                return Action["COMMAND_ON"]
            else:
                return Action["WAIT_REST"]
        else:
            return Action["WAIT_CALL"]

def is_satisfied(sensor_value, set_point, mode):
    if mode == Mode.HEAT:
        return sensor_value > set_point

    elif mode == Mode.COOL:
        return sensor_value < set_point

    else:
        return True

def is_call_for_on(sensor_value, set_point, mode):
    log.debug("is_call_for_on sensor value {} set point {} mode {}".format(sensor_value, set_point, mode))
    if mode == Mode.HEAT:
        return sensor_value < set_point

    elif mode == Mode.COOL:
        return sensor.value > set_point

    else:
        return False


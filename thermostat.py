#!/usr/bin/env python3

from datetime import datetime
import utils as ut
import RPi.GPIO as gpio
import logging

import relay
import rest
from program import Program

logging.basicConfig(filename='phrexia-debug.log', encoding='utf-8', level=logging.DEBUG)
logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger("pyrexia")

last_poll_time = 0
poll_interval = 30


try:
    while True:
        if ut.currentTimeInt() - last_poll_time > poll_interval: 
            last_poll_time = ut.currentTimeInt()

            sensors = rest.get_sensors_list()
            controls = rest.get_controls_list()
            programs = rest.get_programs_list()

            log.debug("sensors {} controls {} programs {}".format(len(sensors), len(controls), len(programs)))

            if len(sensors) > 0 and len(controls) > 0 and len(programs) > 0:


                # run the programs and determine the actions
                for program in programs:
                    sensor = next(x for x in sensors if x.id == program.sensor_id)
                    v = sensor.read_sensor()
                    if v != -999:
                        control = next(x for x in controls if x.id == program.control_id)
                        control.apply_action(sensors, program)

                # execute the actions
                for control in controls:
                    control.command(False)
                    ##control.execute_action()
       
finally:
    print("done")
    try:
        gpio.cleanup()
    except:
        pass



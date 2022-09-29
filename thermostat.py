#!/usr/bin/env python3

from datetime import datetime
import asyncio
import RPi.GPIO as gpio
import logging
import asyncio

import utils as ut
import relay
import rest
from program import Program

logging.basicConfig(filename='pyrexia-debug.log', encoding='utf-8', level=logging.DEBUG)
logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger("pyrexia")

async def main():

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
                        sensor = next((x for x in sensors if program.id == x.id), None)
                        if sensor is None:
                            log.debug("program id {} could not locate sensor id {}".format(program.id, program.sensor_id))
                        elif program.enabled == True:
                            v = await sensor.read_sensor()
                            log.debug("read_sensor {} {} returned {}".format(sensor.name, sensor.id, v))
                            if v > -900:
                                control = next((x for x in controls if x.id == program.control_id), None)
                                if control is None:
                                    log.debug("program id {} could not locate control id {}".format(program.id, program.control_id))

                                control.apply_action(program, sensors)

                    # execute the actions
                    for control in controls:
                        log.debug("control {} action {}".format(control.id, control.action))
                        control.execute_action()
       
    finally:
        log.debug("gpio cleanup")
        try:
            gpio.cleanup()
        except:
           pass

asyncio.run(main())



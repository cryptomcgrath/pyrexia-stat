#!/usr/bin/env python3

from datetime import datetime
import asyncio
import RPi.GPIO as gpio
import logging
import asyncio
import time
import sys

import pyrexia.utils as ut
import pyrexia.relay as relay
import pyrexia.rest as rest
from pyrexia.program import Program
from pyrexia.action import Action

logging.basicConfig(filename='pyrexia-debug.log', encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname).1s %(name)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger("pyrexia")

async def main():

    last_poll_time = 0
    poll_interval = 30

    try:
        # connect
        res = rest.connect()
        if not res.ok:
            fail = "failed to connect to api {}".format(res)
            log.debug(fail)
            sys.exit(fail)
            
        # initialize controls to OFF
        controls = rest.get_controls_list()
        for control in controls:
            control.action = Action.COMMAND_OFF
            log.debug("init control {} -> {}".format(control.id, control.action.name))
            control.execute_action()

        # polling loop
        while True:
            time.sleep(1)
            if ut.currentTimeInt() - last_poll_time > poll_interval:
                connect_res = rest.connect()
                last_poll_time = ut.currentTimeInt()

                if connect_res.ok:
                    sensors = rest.get_sensors_list()
                    controls = rest.get_controls_list()
                    programs = rest.get_programs_list()
                    log.debug("***loop: sensors {} controls {} programs {}".format(len(sensors), len(controls), len(programs)))
                else:
                    log.debug("***loop: unable to connect to api {}".format(connect_res))
                    
                if connect_res.ok and len(sensors) > 0 and len(controls) > 0 and len(programs) > 0:
                    # run the programs and determine the actions
                    for program in programs:
                        sensor = next((x for x in sensors if program.id == x.id), None)
                        if sensor is None:
                            log.debug("program id {} could not locate sensor id {}".format(program.id, program.sensor_id))
                        else:
                            v = 0
                            if program.enabled == True:
                                v = await sensor.read_sensor()
                                log.debug("program id {} sensor id {} ({}) read_sensor returned {}".format(program.id, sensor.id, sensor.name, v))
                            if v > -900:
                                control = next((x for x in controls if x.id == program.control_id), None)
                                if control is None:
                                    log.debug("program id {} could not locate control id {}".format(program.id, program.control_id))

                                control.apply_action(program, sensors)

                    # execute the actions
                    for control in controls:
                        log.debug("control {} execute_action {}".format(control.id, control.action))
                        control.execute_action()
       
    finally:
        log.debug("gpio cleanup")
        try:
            gpio.cleanup()
        except:
           pass

if __name__ == "__main__":
    asyncio.run(main())



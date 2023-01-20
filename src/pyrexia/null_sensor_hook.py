import pyrexia.utils as ut
import pyrexia.rest as rest
from pyrexia.sensor_hook import SensorHook

import logging
import asyncio


logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger("pyrexia")

class NullSensorHook(SensorHook):
    addr = ""

    def __init__(self, addr):
        self.addr = addr

    async def read_sensor(self):
        return -907

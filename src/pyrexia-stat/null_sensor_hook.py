import sensorpush as sp
import utils as ut
import rest
from sensor_hook import SensorHook

import logging
import asyncio


#logging.basicConfig(filename='pyrexia-debug.log', encoding='utf-8', level=logging.DEBUG)
logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger("pyrexia")

class NullSensorHook(SensorHook):
    addr = ""

    def __init__(self, addr):
        self.addr = addr

    async def read_sensor(self):
        return -907

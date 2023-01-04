import sensorpush as sp
import utils as ut
from sensor_hook import SensorHook

import logging

read_error = -999

logging.basicConfig(filename='pyrexia-debug.log', encoding='utf-8', level=logging.DEBUG)
logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger("pyrexia")

class SpSensorHook(SensorHook):
    addr = ""

    def __init__(self, addr):
        self.addr = addr

    def read_sensor(self):
        macaddr = self.addr
        sp.connect(macaddr)

        temp = sp.read_first_value()
        if temp == None:
            return -902
        return float(temp)

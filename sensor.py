import sensorpush as sp
import utils as ut
import rest
from isensor import ISensor

import logging
import asyncio

read_error = -999

logging.basicConfig(filename='phyexia-debug.log', encoding='utf-8', level=logging.DEBUG)
logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger("pyrexia")

class Sensor(ISensor):

    id = 0
    name = ""
    sensor_type = ""
    addr = ""
    update_time = 0
    value = 0.0
    update_interval = 0
    sensor_impl = None

    def __init__(self, id, name, sensor_type, addr, update_time, value, update_interval):
        self.id = id
        self.name = name
        self.sensor_type = sensor_type
        self.addr = addr
        self.update_time = update_time
        self.value = value
        self.update_interval = update_interval

        #sensor_type = addr[0:2]
        #if sensor_type == "sp":
        #    sensor_impl = SpSensor(addr)
        #elif sensor_type == "hw":


    def from_dict(dict):
        sensor_id = dict["id"]
        name = dict["name"]
        sensor_type = dict["sensor_type"]
        addr = dict["addr"]
        update_time = dict["update_time"]
        value = dict["value"]
        update_interval = dict["update_interval"]
        return Sensor(sensor_id, name, sensor_type, addr, update_time, value, update_interval)

    def can_update(self):
        is_interval_met = ut.currentTimeInt() - self.update_time > self.update_interval

        log.debug("can_update {}  {} - {} > {}".format(is_interval_met, ut.currentTimeInt(), self.update_time, self.update_interval))
        return is_interval_met 

    async def read_sensor(self):
        if not self.can_update():
            return -901

        ## is sensorpush addr?
        if self.sensor_type == "sp":
            macaddr = self.addr
            sp.connect(macaddr)

            temp = sp.read_first_value()
            if temp == None:
                return -902
            self.value = float(temp)
            rest.update_sensor_temp(self.id, temp)
            return temp 

        elif self.sensor_type == "gp":
            return -903

        else:
            return -904



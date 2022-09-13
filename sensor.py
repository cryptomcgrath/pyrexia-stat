import sensorpush as sp
import utils as ut
import rest

import logging
import asyncio

read_error = -999

logging.basicConfig(filename='phrexia-debug.log', encoding='utf-8', level=logging.DEBUG)
logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger("pyrexia")

class Sensor:

    id = 0
    name = ""
    addr = ""
    update_time = 0
    value = 0.0
    update_interval = 0

    def __init__(self, id, name, addr, update_time, value, update_interval):
        self.id = id
        self.name = name,
        self.addr = addr
        self.update_time = update_time
        self.value = value
        self.update_interval = update_interval


    def from_dict(dict):
        sensor_id = dict["id"]
        name = dict["name"]
        addr = dict["addr"]
        update_time = dict["update_time"]
        value = dict["value"]
        update_interval = dict["update_interval"]
        return Sensor(sensor_id, name, addr, update_time, value, update_interval)

    def can_update(self):
        is_interval_met = ut.currentTimeInt() - self.update_time > self.update_interval

        log.debug("can_update {}  {} - {} > {}".format(is_interval_met, ut.currentTimeInt(), self.update_time, self.update_interval))
        return is_interval_met 

    async def read_sensor(self):
        if not self.can_update():
            return -901

        ## is sensorpush addr?
        sensor_type = self.addr[0:2]
        if sensor_type == "sp":
            macaddr = self.addr[3:]
            sp.connect(macaddr)

            temp = sp.read_first_value()
            if temp == None:
                return -902
            self.value = temp
            rest.update_sensor_temp(self.id, temp)
            return temp 

        elif sensor_type == "gp":
            return -903

        else:
            return -904



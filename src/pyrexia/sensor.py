import pyrexia.utils as ut
import pyrexia.rest as rest
from pyrexia.sensor_hook import SensorHook
from pyrexia.sp_sensor_hook import SpSensorHook
from pyrexia.null_sensor_hook import NullSensorHook
from pyrexia.dht_sensor_hook import DhtSensorHook

import logging
import asyncio

read_error = -999

logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger("pyrexia")

class Sensor:

    id = 0
    name = ""
    sensor_type = ""
    addr = ""
    update_time = 0
    value = 0.0
    update_interval = 0
    hook = None

    def __init__(self, id, name, sensor_type, addr, update_time, value, update_interval):
        self.id = id
        self.name = name
        self.sensor_type = sensor_type
        self.addr = addr
        self.update_time = update_time
        self.value = value
        self.update_interval = update_interval

        if sensor_type == "sp":
            self.hook = SpSensorHook(addr)
        elif sensor_type == "dht22":
            self.hook = DhtSensorHook(addr)
        else:
            self.hook = NullSensorHook(addr)


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

        log.debug("can_update {}  {} - {} > {} = {}".format(is_interval_met, ut.currentTimeInt(), self.update_time, self.update_interval, is_interval_met))
        return is_interval_met 

    async def read_sensor(self):
        if not self.can_update():
            return -901

        t = await self.hook.read_sensor()
        if t > -900:
            self.value = t
            self.update_time = ut.currentTimeInt()
            rest.update_sensor_temp(self.id, t)
        return t


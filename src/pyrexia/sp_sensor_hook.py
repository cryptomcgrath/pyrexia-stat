from sensorpush import sensorpush as sp
import pyrexia.utils as ut
from pyrexia.sensor_hook import SensorHook
from bleak import BleakClient
import asyncio

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger("pyrexia")

class SpSensorHook(SensorHook):
    _addr = ""

    def __init__(self, addr):
        self._addr = addr

    async def read_sensor(self):
        client = BleakClient(self._addr)
        temp_f = -902
        try:
            await client.connect()
            temp_c = await sp.read_temperature(client)
            temp_f = ut.celsiusToFahrenheit(temp_c)
        except Exception as e:
            logging.exception("problem reading sensor")
        finally:
            await client.disconnect()
            return temp_f


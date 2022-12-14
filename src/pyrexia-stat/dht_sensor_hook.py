import sensorpush as sp
import utils as ut
import rest
from sensor_hook import SensorHook

import logging
import asyncio
import Adafruit_DHT


logging.basicConfig(filename='pyrexia-debug.log', encoding='utf-8', level=logging.DEBUG)
logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger("pyrexia")

class DhtSensorHook(SensorHook):
    gpio_pin = None
    sensor = None

    def __init__(self, addr):
        pin = int(addr)
        if pin < 0 or pin >40:
            raise Exception("invalid gpio pin specified for DHT22")
        self.gpio_pin = pin
        self.sensor = Adafruit_DHT.DHT22

    def read_sensor(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.gpio_pin)
        if humidity is None or temperature is None:
            return -911
        return ut.celsiusToFahrenheit(temperature)

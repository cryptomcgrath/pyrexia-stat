import RPi.GPIO as gpio
import logging
from pyrexia.irelay import IRelay

#logging.basicConfig(filename='pyrexia-debug.log', encoding='utf-8', level=logging.DEBUG)
logging.getLogger(__name__).addHandler(logging.NullHandler())
log = logging.getLogger("pyrexia")

class Relay(IRelay):
    on = gpio.HIGH
    off = gpio.LOW
    gpio_id = 0
    onhigh = True

    def __init__(self, gpio_id, onhigh):
        self.gpio_id = gpio_id
        gpio.setmode(gpio.BCM)
        gpio.setup(gpio_id, gpio.OUT)

        if onhigh == True or onhigh == 1:
            self.onhigh = True
            self.on = gpio.HIGH
            self.off = gpio.LOW
        else: 
            self.onhigh = False
            self.on = gpio.LOW
            self.off = gpio.HIGH

    def command(self, onoff):
        if onoff == True:
            log.debug("relay gpio {} set to {}".format(self.gpio_id, self.on))
            gpio.output(self.gpio_id, self.on)
        else:
            log.debug("relay gpio {} set to {}".format(self.gpio_id, self.off))
            gpio.output(self.gpio_id, self.off)

    def is_on(self):
        if self.onhigh == True:
            return gpio.input(self.gpio_id) == gpio.HIGH
        else:
            return gpio.input(self.gpio_id) == gpio.LOW


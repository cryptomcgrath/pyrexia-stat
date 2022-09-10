import RPi.GPIO as gpio

class Relay:
    on = gpio.HIGH
    off = gpio.LOW
    id = 0
    onhigh = True

    def __init__(self, id, onhigh):
        self.id = id
        gpio.setmode(gpio.BCM)
        gpio.setup(id, gpio.OUT)

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
            gpio.output(self.id, self.on)
        else:
            gpio.output(self.id, self.off)

    def is_on(self):
        if self.onhigh == True:
            return gpio.input(self.id) == gpio.HIGH
        else:
            return gpio.input(self.id) == gpio.LOW


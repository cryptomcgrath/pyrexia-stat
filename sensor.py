import sensorpush
import utils as ut

read_error = -999

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
        self.addr
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
        return ut.currentTimeInt() - self.update_time > self.update_interval


    def read_sensor(self):
        if self.can_update():
            return -999

        ## is sensorpush addr?
        if addr[0:2] == "sp":
            addr = addr[3:]
            sp.connect(addr)

            def cb(ts, temp):
                print("sensor id {} temp={}".format(sensor_id, temp))
                value = temp
                rest.update_sensor_temp(sensor_id, temp)
                return temp

            try:
                sp.read_latest(cb)
            except:
                return read_error

        return read_error 




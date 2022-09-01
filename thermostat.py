import sensor as sp
from datetime import datetime
import utils as ut
from tinydb import TinyDB, Query
import init_db as db

last_poll_time = 0
poll_interval = 30


def update_sensors():
    sensor_db = TinyDB(db.SENSOR_DB_FILENAME)
    sensors = sensor_db.all()
    for sensor in sensors:
        print(sensor)
        update_time = sensor["update_time"]
        update_interval = sensor["update_interval"]
        if ut.currentTimeInt() - update_time > update_interval:
        
            if sensor["type"][0:2] == "sp":
                addr = sensor["type"][3:]
                sp.connect(addr)
            
                def cb(ts, temp):
                    print("temp={}".format(temp))                 
                    save_temp(sensor["name"], temp)
                sp.read_latest(cb)

def save_temp(name, temp):
    sensor_db = TinyDB(db.SENSOR_DB_FILENAME)
    rec = Query()
    sensor_db.update({'value': temp, 'update_time': ut.currentTimeInt() }, rec.name == name)

def check_programs():
    program_db = TinyDB(db.PROGRAM_DB_FILENAME)
    programs = program_db.all()
    for program in programs:
        if program["enabled"]:
            name = program["name"]
            print("program {} enabled".format(name))

while True:
    if ut.currentTimeInt() - last_poll_time > poll_interval: 
        last_poll_time = ut.currentTimeInt()

        update_sensors()
        check_programs()



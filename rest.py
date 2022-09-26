import utils as ut
import requests
import json
import logging

from sensor import Sensor
from control import Control
from program import Program

logging.basicConfig(filename='pyrexia-debug.log', encoding='utf-8', level=logging.DEBUG)
logging.getLogger(__name__).addHandler(logging.NullHandler())

log = logging.getLogger("pyrexia")

base_url = "http://192.168.0.119:8000"

def get_sensors():
    url = base_url + "/sensors"
    res = requests.get(url)
    if res.ok:
        jData = json.loads(res.content)
        return jData
    else:
        return -1

def update_sensor_temp(id, temp):
    url = base_url + "/sensors/"+str(id)+"/temp" 
    update_time = ut.currentTimeInt()
    obj = {'value': temp, 'update_time': update_time}
    res = requests.post(url, json = obj)
    return res

def get_programs():
    url = base_url + "/programs"
    res = requests.get(url)
    if res.ok:
        jData = json.loads(res.content)
        return jData
    else:
        return -1

def get_controls():
    url = base_url + "/controls"
    res = requests.get(url)
    if res.ok:
        json_data = json.loads(res.content)
        return json_data
    else:
        return -1

def get_sensors_list():
    sensors = []
    try:
        sensors_dict = get_sensors()
        for sensor_dict in sensors_dict["data"]:
            sensor = Sensor.from_dict(sensor_dict)
            sensors.append(sensor)
    except:
        log.exception("error getting sensors")
        pass

    return sensors

def get_controls_list():
    controls = []
    try:
        controls_dict = get_controls()
        for control_dict in controls_dict["data"]:
            control = Control.from_dict(control_dict)
            controls.append(control)
    except:
        log.exception("error getting controls")
        pass

    return controls
  
def get_programs_list():
    programs = []
    try:
        programs_dict = get_programs()
        for program_dict in programs_dict["data"]:
            program = Program.from_dict(program_dict)        
            programs.append(program)
    except:
        log.exception("error getting programs")
        pass

    return programs

def add_history(program_id, set_point, sensor_id, sensor_value, control_id, control_on, action):
    print("{} {} {} {} {} {}".format(program_id, sensor_id, sensor_value, control_id, control_on, action))
    url = base_url + "/history/"
    update_time = ut.currentTimeInt()
    obj = {'program_id': program_id, 'set_point': set_point, 'action_ts': update_time, 'sensor_id': sensor_id, 'sensor_value': sensor_value, 'control_id': control_id, 'control_on': int(control_on==True), 'action': action}
    print("{}".format(obj))
    res = requests.post(url, json = obj)
    return res

     

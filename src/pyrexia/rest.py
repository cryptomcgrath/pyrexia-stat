import pyrexia.utils as ut
import requests
import json
import logging
import pyrexia.config as config

from pyrexia.sensor import Sensor
from pyrexia.control import Control
from pyrexia.program import Program

#logging.basicConfig(filename='pyrexia-debug.log', encoding='utf-8', level=logging.DEBUG)
logging.getLogger(__name__).addHandler(logging.NullHandler())

log = logging.getLogger("pyrexia")

base_url = config.base_url

def get_headers():
  return {"Content-Type":"application/json", "x-access-token":token}

def login(user, password):
    url = base_url + "/users/login"
    obj = {'email': user, 'password':password}
    res = requests.post(url, json = obj)
    if res.ok:
        data = res.json()
        global token
        if "token" in data:
            token = data["token"]
            log.debug("login success")
        else:
            token = ""
    return res

def register_device(user, password):
    url = base_url + "/users/register"
    obj = {'email': user, 'password':password, 'admin':'true'}
    res = requests.post(url, json = obj)
    if res.ok:
        config.mark_registered()
    return res

def connect():
    if config.login_registered == "N":
        reg_res = register_device(config.login_user, config.login_password)
        if not reg_res.ok:
            return reg_res
    res = login(config.login_user, config.login_password)
    return res

def get_sensors():
    url = base_url + "/sensors"
    res = requests.get(url, headers=get_headers())
    if res.ok:
        jData = json.loads(res.content)
        return jData
    else:
        return -1

def update_sensor_temp(id, temp):
    url = base_url + "/sensors/"+str(id)+"/temp" 
    update_time = ut.currentTimeInt()
    obj = {'value': temp, 'update_time': update_time}
    res = requests.post(url, headers=get_headers(), json=obj)
    return res

def control_on(id):
    url = base_url + "/controls/"+str(id)+"/on"
    res = requests.post(url, headers=get_headers())

def control_off(id):
    url = base_url + "/controls/"+str(id)+"/off"
    res = requests.post(url, headers=get_headers())

def update_program_action(id, action):
    url = base_url + "/programs/"+str(id)+"/action"
    obj = {'action': action}
    res = requests.post(url, json = obj, headers=get_headers())
    return res

def get_programs():
    url = base_url + "/programs"
    res = requests.get(url, headers=get_headers())
    if res.ok:
        jData = json.loads(res.content)
        return jData
    else:
        return -1

def get_controls():
    url = base_url + "/controls"
    res = requests.get(url, headers=get_headers())
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

def add_history(program_id, set_point, sensor_id, sensor_value, control_id, control_on, program_action, control_action):
    url = base_url + "/history/"
    update_time = ut.currentTimeInt()
    obj = {'program_id': program_id, 'set_point': set_point, 'action_ts': update_time, 'sensor_id': sensor_id, 'sensor_value': sensor_value, 'control_id': control_id, 'control_on': int(control_on==True), 'program_action': program_action, 'control_action': control_action}
    print("{}".format(obj))
    res = requests.post(url, json = obj, headers=get_headers())
    return res

def user_register(email, password):
    url = base_url + "/users/register"
    obj = {'email': email, 'password':password}
    res = requests.post(url, json = obj)
    return res     

def ping(url):
    url = url + "/setup/ping"
    try:
        res = requests.get(url)
        return res
    except:
        return None

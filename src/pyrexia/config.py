from configparser import ConfigParser
import uuid
import random
import string

CONFIG_FILENAME="pyrexia-config.ini"

#Read config file
config_object = ConfigParser()
config_object.read(CONFIG_FILENAME)

#Get the API section
try:
    api_section = config_object["API"]
except:
    config_object["API"] = {
        "BASE_URL": "http://localhost:8000",
        "LOGIN_USER": "",
        "LOGIN_PASSWORD": "",
        "LOGIN_REGISTERED": "N"
    }
    api_section = config_object["API"]

def write_config():
    #Write changes back to file
    with open(CONFIG_FILENAME, 'w') as conf:
        config_object.write(conf)

def get_device_id():
    return hex(uuid.getnode())

def gen_password():
    # get random password pf length 8 with letters, digits, and symbols
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(16))
    return password

def mark_registered():
    login_registered = "Y"
    api_section["LOGIN_REGISTERED"] = login_registered
    write_config()

# flag if we have updates to write to config
updated = False

base_url = api_section["BASE_URL"]
if (base_url == ""):
    base_url = "http://localhost:8000"
    api_section["BASE_URL"] = base_url
    updated = True

login_user = api_section["LOGIN_USER"]
login_password = api_section["LOGIN_PASSWORD"]
login_registered = api_section["LOGIN_REGISTERED"]
if (login_user  == "" and login_password == ""):
    login_user = get_device_id() + "@pyrexia-stat.app"
    api_section["LOGIN_USER"] = login_user
    login_password = gen_password()
    api_section["LOGIN_PASSWORD"] = login_password
    login_registered = "N"
    api_section["LOGIN_REGISTERED"] = login_registered
    update = True
    
if updated:
    write_config()

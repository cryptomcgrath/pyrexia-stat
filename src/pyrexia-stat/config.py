from configparser import ConfigParser
import uuid
import random
import string

#Read config.ini file
config_object = ConfigParser()
config_object.read("config.ini")

#Get the API section
api_section = config_object["API"]

def write_config():
    #Write changes back to file
    with open('config.ini', 'w') as conf:
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
if (not base_url):
    base_url = "http://localhost:8000"
    api_section["BASE_URL"] = base_url
    updated = True

login_user = api_section["LOGIN_USER"]
login_password = api_section["LOGIN_PASSWORD"]
login_registered = api_section["LOGIN_REGISTERED"]
if (not login_user and not login_password):
    login_user = get_device_id() + "@pyrexia-stat.app"
    api_section["LOGIN_USER"] = login_user
    login_password = gen_password()
    api_section["LOGIN_PASSWORD"] = login_password
    login_registered = "N"
    api_section["LOGIN_REGISTERE"] = login_registered
    update = True
    
if updated:
    write_config()

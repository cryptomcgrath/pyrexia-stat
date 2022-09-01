from tinydb import TinyDB, Query

SENSOR_DB_FILENAME="sensors_db.json"
CONTROL_DB_FILENAME="controls_db.json"
PROGRAM_DB_FILENAME="program_db.json"

def init():
    sensor_db = TinyDB(SENSOR_DB_FILENAME)
    sensor_db.truncate()
    sensor_db.insert({'name': 'valvebay', 'type': 'sp/A4:34:F1:7F:CD:D8', 'update_time': 0, 'value': 0, 'update_interval': 300})

    control_db = TinyDB(CONTROL_DB_FILENAME)
    control_db.truncate()
    control_db.insert({'name': 'suburban18k', 'type': 'heat', 'min_rest': 180, 'last_off_time': 0, 'last_on_time': 0, 'min_run': 180, 'gpio': 17, 'gpio_on_hi': True})


    program_db = TinyDB(PROGRAM_DB_FILENAME)
    program_db.truncate()
    program_db.insert({'name': 'heat', 'enabled': True, 'sensor': 'valvebay', 'value': 55})

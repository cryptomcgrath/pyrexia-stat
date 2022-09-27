// create app
var express = require("express")
var db = require("../database.js")
var md5 = require("md5")

const router = express.Router()

var bodyParser = require("body-parser")
router.use(bodyParser.urlencoded({ extended: false }))
router.use(bodyParser.json())

// create database
router.post("/init", (req, res, next) => {
    db.serialize(()=>{
        // users
        db.run('drop table if exists user')
        db.run('CREATE TABLE user ( id INTEGER PRIMARY KEY AUTOINCREMENT, email text UNIQUE, password text, access_level INTEGER, CONSTRAINT email_unique UNIQUE(email))')
        var insert = 'INSERT INTO user (email, password) VALUES (?,?)'
        db.run(insert, ["edward@edwardmcgrath.com", md5("test1234")])

        // sensors
        db.run('drop table if exists sensors')
        db.run('CREATE TABLE sensors (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, sensor_type text, addr text, update_time integer, value float, update_interval integer)')
        var insert = 'INSERT INTO sensors (name, sensor_type, addr, update_time, value, update_interval) VALUES (?, ?, ?, ?, ?, ?)'
        db.run(insert, ['valve bay', 'sp', 'A4:34:F1:7F:CD:D8', 0, 0, 300])

        // controls
        db.run('drop table if exists controls')
        db.run('CREATE TABLE controls (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, min_rest INT, last_off_time INT, last_on_time INT, min_run INT, gpio INT, gpio_on_hi bool, control_on bool)')

        var insert = 'INSERT INTO controls (name, min_rest, last_off_time, last_on_time, min_run, gpio, gpio_on_hi. control_on) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        db.run(insert, ['furnace', 180, 0, 0, 180, 5, true, false])

        // programs
        db.run('drop table if exists programs')
        db.run('CREATE TABLE programs (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, mode text, enabled bool, sensor_id INTEGER, set_point FLOAT, control_id INT)') 	
        var insert = 'INSERT INTO PROGRAMS (name, mode, enabled, sensor_id, set_point, control_id) VALUES (?, ?, ?, ?, ?, ?)'
        db.run(insert, ['valve bay', 'heat', true, 1, 65.0, 1])

        // history
        db.run('drop table if exists history')
        db.run('CREATE TABLE history (id INTEGER PRIMARY KEY AUTOINCREMENT, program_id INT, set_point FLOAT, action_ts INT, sensor_id INT, sensor_value float, control_id INT, control_on bool, action TEXT)')

        db.run('drop table if exists config')
        db.run('CREATE TABLE config (key text, value text)')
        var insert = 'insert into config (key, value) values (?,?)'
        db.run(insert, ['units', 'f'])
        db.run(insert, ['weather_refresh_secs', '1000'])
        db.run(insert, ['openweather_apikey', '24fc7c899cfe76e81071ef08550b62c6'])
        db.run(insert, ['poll_interval', '30'])
        res.json({"message": "Ok"})
    })

})

router.get("/config", (req, res, next) => {
    var sql = "select * from config"
    var params = []
    db.all(sql, params, (err, rows) => {
        if (err) {
            res.status(400).json({"error":err.message})
            return
        }
        res.json({
            "message":"success",
            "data":rows
        })
    })
})



module.exports = router


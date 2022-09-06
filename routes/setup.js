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
        db.run('CREATE TABLE sensors (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, addr text, update_time integer, value float, update_interval integer)')
        var insert = 'INSERT INTO sensors (name, addr, update_time, value, update_interval) VALUES (?, ?, ?, ?, ?)'
        db.run(insert, ['valve bay', 'sp/A4:34:F1:7F:CD:D8', 0, 0, 300])

        // controls
        db.run('drop table if exists controls')
        db.run('CREATE TABLE controls (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, min_rest INT, last_off_time INT, last_on_time INT, min_run INT, gpio INT, gpio_on_hi bool)')
        var insert = 'INSERT INTO controls (name, min_rest, last_off_time, last_on_time, min_run, gpio, gpio_on_hi) VALUES (?, ?, ?, ?, ?, ?, ?)'
        db.run(insert, ['furnace', 180, 0, 0, 180, 17, true])

        // programs
        db.run('drop table if exists programs')
        db.run('CREATE TABLE programs (id INTEGER PRIMARY KEY AUTOINCREMENT, name text, type text, enabled bool, sensor_id INTEGER, value FLOAT)') 	
        var insert = 'INSERT INTO PROGRAMS (name, type, enabled, sensor_id, value) VALUES (?, ?, ?, ?, ?)'
        db.run(insert, ['heat', 'heat', true, 1, 0.0])

        res.json({"message": "Ok"})
    })

})


module.exports = router


// create app
var express = require("express")
var db = require("../database.js")
var md5 = require("md5")

const router = express.Router()

var bodyParser = require("body-parser")
router.use(bodyParser.urlencoded({ extended: false }))
router.use(bodyParser.json())


router.get("/", (req, res, next) => {
    var sql = "select * from history"
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


router.post("/", (req, res, next) => {
    var errors=[]
    if (!req.body.program_id){
        errors.push("No program_id specified")
    }
    if (!req.body.control_id){
        errors.push("No control_id specified")
    }
    if (!req.body.sensor_id){
        errors.push("No sensor_id specified")
    }
    if (!req.body.sensor_value){
        errors.push("No sensor_value specified")
    }
    //if (req.body.control_on != 0 and req.body.control_on != 1){ 
    //    errors.push("control_on must be 1 or 0")
    //}
    if (!req.body.action_ts){
        errors.push("No action_ts specified")
    }
    if (!req.body.action) {
        errors.push("No action specified")
    }

    if (errors.length){
        res.status(400).json({"error":errors.join(",")})
        return
    }
    var data = {
        program_id: req.body.program_id,
        set_point: req.body.set_point,
        control_id: req.body.control_id,
        sensor_id: req.body.sensor_id,
        sensor_value: req.body.sensor_value,
        control_on: req.body.control_on,
        action_ts: req.body.action_ts,
        action: req.body.action
    }
    var sql ='INSERT INTO history (program_id, set_point, control_id, sensor_id, sensor_value, control_on, action_ts, action) values (?,?,?,?,?,?,?,?)'
    var params =[data.program_id, data.set_point, data.control_id, data.sensor_id, data.sensor_value, data.control_on, data.action_ts, data.action]
    db.run(sql, params, function (err, result) {
        if (err){
            res.status(400).json({"error": err.message})
            return
        }
        res.json({
            "message": "success",
            "data": data,
            "id" : this.lastID
        })
    })
})

module.exports = router


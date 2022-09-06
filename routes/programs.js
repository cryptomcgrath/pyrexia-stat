// create app
var express = require("express")
var db = require("../database.js")
var md5 = require("md5")

const router = express.Router()

var bodyParser = require("body-parser")
router.use(bodyParser.urlencoded({ extended: false }))
router.use(bodyParser.json())


router.get("/", (req, res, next) => {
    var sql = "select * from programs"
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

router.get("/:id", (req, res, next) => {
    var sql = "select * from programs where id = ?"
    var params = [req.params.id]
    db.get(sql, params, (err, row) => {
        if (err) {
          res.status(400).json({"error":err.message})
          return
        }
        res.json({
            "message":"success",
            "data":row
        })
      })
})


router.post("/", (req, res, next) => {
    var errors=[]
    if (!req.body.name){
        errors.push("Missing name")
    }
    if (!req.body.type){
        errors.push("Missing type")
    }
    if (!req.body.enabled){
        errors.push("Missing enabled")
    }
    if (!req.body.sensor_id){
        errors.push("Missing sensor_id")
    }
    if (!req.body.value){
        errors.push("Missing value")
    }
    if (errors.length){
        res.status(400).json({"error":errors.join(",")})
        return
    }
    var data = {
        name: req.body.name,
        type: req.body.type,
        enabled: req.body.enabled,
        sensor_id: req.body.sensor_id,
        value: req.body.value
    }
    var sql ='INSERT INTO programs (name, type, enabled, sensor_id, value) VALUES (?,?,?,?,?)'
    var params =[data.name, data.type, data.enabled, data.sensor_id, data.value]
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

router.patch("/:id", (req, res, next) => {
    var data = {
        name: req.body.name,
        min_rest: req.body.min_rest,
        last_off_time: req.body.last_off_time,
        last_on_time: req.body.last_on_time,
        min_run: req.body.min_run,
        gpio: req.body.gpio,
        gpio_on_hi: req.body.gpio_on_hi
    }
    db.run(
        `UPDATE programs set 
           name = COALESCE(?,name), 
           type = COALESCE(?,type), 
           enabled = COALESCE(?,enabled) 
           sensor_id = COALESCE(?,sensor_id)
           value = COALESCE(?,value)
           WHERE id = ?`,
        [data.name, data.type, data.enabled, data.sensor_id, data.value, params.id],

        function (err, result) {
            if (err){
                res.status(400).json({"error": res.message})
                return
            }
            res.json({
                message: "success",
                data: data,
                changes: this.changes
            })
    })
})

router.delete("/:id", (req, res, next) => {
    db.run(
        'DELETE FROM programs WHERE id = ?',
        req.params.id,
        function (err, result) {
            if (err){
                res.status(400).json({"error": res.message})
                return
            }
            res.json({"message":"deleted", changes: this.changes})
    })
})


module.exports = router


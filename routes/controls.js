// create app
var express = require("express")
var db = require("../database.js")
var md5 = require("md5")

const router = express.Router()

var bodyParser = require("body-parser")
router.use(bodyParser.urlencoded({ extended: false }))
router.use(bodyParser.json())


router.get("/", (req, res, next) => {
    var sql = "select * from controls"
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
    var sql = "select * from controls where id = ?"
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
    if (!req.body.min_rest){
        errors.push("Missing min_rest")
    }
    if (!req.body.last_off_time){
        errors.push("Missing last_off_time")
    }
    if (!req.body.last_on_time){
        errors.push("Missing last_on_time")
    }
    if (!req.body.min_run){
        errors.push("Missing min_run")
    }
    if (!req.body.gpio){
        errors.push("Missing gpio")
    }
    if (!req.body.gpio_on_hi){
        errors.push("Missing gpio_on_hi")
    }
    if (errors.length){
        res.status(400).json({"error":errors.join(",")})
        return
    }
    var data = {
        name: req.body.name,
        min_rest: req.body.min_rest,
        last_off_time: req.body.last_off_time,
        last_on_time: req.body.last_on_time,
        min_run: req.body.min_run,
        gpio: req.body.gpio,
        gpio_on_hi: req.body.gpio_on_hi
    }
    var sql ='INSERT INTO programs (name, min_rest, last_off_time, last_on_time, min_run, gpio, gpio_on_hi) VALUES (?,?,?,?,?,?,?)'
    var params =[data.name, data.min_rest, data.last_off_time, data.last_on_time, data.min_run, data.gpio, data.gpio_on_hi]
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
        `UPDATE controls set 
           name = COALESCE(?,name), 
           min_rest = COALESCE(?,min_rest), 
           last_off_time = COALESCE(?,last_off_time) 
           last_on_time = COALESCE(?,last_on_time)
           min_run = COALESCE(?,min_run)
           gpio = COALESCE(?,gpio)
           gpio_on_hi = COALESCE(?,gpio_on_hi)
           WHERE id = ?`,
        [data.name, data.min_rest, data.last_off_time, data.last_on_time, data.min_run, data.gpio, data.gpio_on_hi, params.id],
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
        'DELETE FROM controls WHERE id = ?',
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


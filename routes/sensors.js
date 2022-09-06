// create app
var express = require("express")
var db = require("../database.js")
var md5 = require("md5")

const router = express.Router()

var bodyParser = require("body-parser")
router.use(bodyParser.urlencoded({ extended: false }))
router.use(bodyParser.json())


router.get("/", (req, res, next) => {
    var sql = "select * from sensors"
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
    var sql = "select * from sensors where id = ?"
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
        errors.push("No name specified")
    }
    if (!req.body.addr){
        errors.push("No addr specified")
    }
    if (!req.body.update_time) {
        errors.push("Missing update_time")
    }
    if (!req.body.value) {
        errors.push("Missing value")
    }
    if (!req.body.update_interval) {
        errors.push("Missing update_interval")
    }
    if (errors.length){
        res.status(400).json({"error":errors.join(",")})
        return
    }
    var data = {
        name: req.body.name,
        addr: req.body.addr,
        update_time: req.body.update_time,
        value: req.body.value,
        update_interval: req.body.update_interval
    }
    var sql ='INSERT INTO sensors (name, addr, update_time) VALUES (?,?,?,?,?)'
    var params =[data.name, data.addr, data.update_time, date.value, data.update_interval]
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
        addr: req.body.addr,
        update_time : req.body.update_time,
        value: req.body.value,
        update_interval: req.body.update_interval
    }
    db.run(
        `UPDATE sensors set 
           name = COALESCE(?,name), 
           addr = COALESCE(?,addr), 
           update_time = COALESCE(?,update_time),
           value = COALESCE(?,value),
           update_interval = COALESCE(?, update_interval)
           WHERE id = ?`,
        [data.name, data.email, data.update_time, data.value, data.update_interval, req.params.id],
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
        'DELETE FROM user WHERE id = ?',
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


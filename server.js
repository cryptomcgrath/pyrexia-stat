// create app
var express = require("express")
var app = express()
var db = require("./database.js")
var md5 = require("md5")

const usersRouter = require('./routes/users.js')
const sensorsRouter = require('./routes/sensors.js')
const setupRouter = require('./routes/setup.js')
const controlsRouter = require('./routes/controls.js')
const programsRouter = require('./routes/programs.js')

// server listen
var PORT = 8000
app.listen(PORT, ()=> {
    console.log("Server running on %PORT%".replace("%PORT%", PORT))
})

// root endpoint
app.get("/", (req, res, next) => {
    res.json({"message": "Ok"})
})

app.use('/users', usersRouter)
app.use('/sensors', sensorsRouter)
app.use('/setup', setupRouter)
app.use('/controls', controlsRouter)
app.use('/programs', programsRouter)

// default response for any other request
app.use(function(req, res) {
    res.status(404)
})



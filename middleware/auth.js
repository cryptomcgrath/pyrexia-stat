var db = require("../database.js")
var createError = require("http-errors")

checkNotAlreadyRegistered = (req, res, next) => {
  db.get("select * from user limit 1", (err, row) => {
    if (!err && !row) {
      next()
    }
    next(createError(403, "Not authorized"))
  })
}

const auth = {
  checkNotAlreadyRegistered
}

module.exports = auth

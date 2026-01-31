const mongoose = require('mongoose')

module.exports = () => {
    mongoose.connect("mongodb://127.0.0.1:27017/userDB")
.then(() => console.log("MongoDB Connected!!!!!"))
.catch(err => console.log("DB Error:", err))
}
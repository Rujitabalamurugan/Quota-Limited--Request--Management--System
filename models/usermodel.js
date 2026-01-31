const mongoose = require('mongoose')

module.exports = () => {
    mongoose.connect("mongodb://127.0.0.1:27017/userDB")
.then(() => console.log("MongoDB Connected!!!!!"))
.catch(err => console.log("DB Error:", err))
}
const userSchema = new mongoose.Schema({
    name: String,
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true, minlength: [8, "Password must be at least 8 characters long"] },
    role: { type: String, default: "USER" },
    age: Number,
    requestQuota: { type: Number, default: 5 }
})
const mongoose = require('mongoose')


const userSchema = new mongoose.Schema({
    name: String,
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true, minlength: [8, "Password must be at least 8 characters long"] },
    role: { type: String, default: "USER" },
    age: Number,
    requestQuota: { type: Number, default: 5 }
})

module.exports = mongoose.model("User", userSchema)
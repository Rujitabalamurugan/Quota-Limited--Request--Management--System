require('dotenv').config()

const express = require('express')
const router = express.Router()
const bcrypt = require('bcrypt')    
const User = require('../models/usermodel')
const jwt = require('jsonwebtoken')
 const secretcode = "rujitabalamurugan"
router.post('/signup', async (req, res) => {
    try {
        const { name, email, role, age, password } = req.body
        if (!email || !password) return res.status(400).json({ message: "Email and password required" })

        const existingUser = await User.findOne({ email })
        if (existingUser) return res.status(400).json({ message: "User already exists" })

        const hashPassword = await bcrypt.hash(password, 10)

        const user = new User({ name, email, role, age, password: hashPassword })
        await user.save()

        res.status(201).json({ message: "User registered in Quota-Limited Request Management System" })
    } catch (err) {
        res.status(500).json({ message: "Server Error", error: err.message })
    }
})

module.exports = router
router.post('/login', async (req, res) => {
    const user = await User.findOne({ email: req.body.email })
    if (!user) return res.json({ message: "Email is invalid" })

    const isPasswordmatch = await bcrypt.compare(req.body.password, user.password)
    if (!isPasswordmatch) return res.json({ message: "Password is incorrect" })

    const token = jwt.sign({ id: user._id }, process.env.SECRET_CODE, { expiresIn: "1h" })
    return res.json({ message: "Login Successful in Quota-Limited Request Management System", token: token })
})

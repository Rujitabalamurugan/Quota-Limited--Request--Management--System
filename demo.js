const mongoose = require("mongoose")
const express = require("express")
const bcrypt = require("bcrypt")

const app = express()
app.use(express.json())

mongoose.connect("mongodb://127.0.0.1:27017/test-db")
.then(() => console.log(" MongoDB Connected"))
.catch(err => console.log(" DB Error:", err))



const userSchema = new mongoose.Schema({
    firstName: { type: String, required: true },
    lastName: { type: String, required: true },
    username: { type: String, required: true, unique: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
    bio: { type: String, default: "" }
})

const User = mongoose.model("useraccount", userSchema)



app.post('/users/signup', async (req, res) => {
    try {
        const { firstName, lastName, username, email, password, bio } = req.body

        
        if (!firstName || !lastName || !username || !email || !password) {
            return res.status(400).json({ message: "All required fields must be filled" })
        }

        
        const existingUser = await User.findOne({
            $or: [{ email }, { username }]
        })

        if (existingUser) {
            return res.status(400).json({ message: "Email or Username already exists" })
        }

        
        const hashedPassword = await bcrypt.hash(password, 10)

        
        const user = new User({
            firstName,
            lastName,
            username,
            email,
            password: hashedPassword,
            bio
        })

        await user.save()

        res.status(201).json({ message: " User registered successfully" })

    } catch (err) {
        res.status(500).json({ message: "Server Error", error: err.message })
    }
})


app.listen(3000, () => {
    console.log(" Server running on http://localhost:3000")
})

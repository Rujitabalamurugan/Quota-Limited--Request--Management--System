require('dotenv').config();
const mongoose = require('mongoose');

module.exports = () => {
mongoose.connect(process.env.DB_URL)
.then(() => console.log("MongoDB Connected!!!!!"))
.catch(err => console.log("DB Error:", err))
}
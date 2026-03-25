import bcrypt
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb+srv://rujitabalamurugan_db_user:Rujita%4029@cluster0.gfxrofb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["contact_system"]
users = db["users"]

email = "admin@system.com"
password = "password"

if not users.find_one({"email": email}):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users.insert_one({
        "name": "System Admin", 
        "email": email, 
        "password_hash": hashed_password.decode('utf-8'), 
        "created_at": datetime.now()
    })
    print(f"Created user: {email} with password: {password}")
else:
    print(f"User {email} already exists. You can log in using that email.")

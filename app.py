from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import joblib
from datetime import datetime, time
from bson.objectid import ObjectId
app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://localhost:27017/")
db = client["contact_system"]
collection = db["messages"]

model = joblib.load("spam_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")
import bcrypt

users_collection = db["users"]


@app.route("/submit", methods=["POST"])
def submit():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    today_start = datetime.combine(datetime.now().date(), time.min)
    today_end = datetime.combine(datetime.now().date(), time.max)
    
    request_count = collection.count_documents({
        "email": email,
        "date": {"$gte": today_start, "$lte": today_end}
    })
    
    if request_count >= 5:
        return jsonify({"error": "Quota Exceeded. Limit of 5 requests per day."}), 429

    message = data.get("message", "")
    text = vectorizer.transform([message])
    prediction = model.predict(text)

    status = "Spam" if prediction[0] == 1 else "Pending"

    doc = {
        "name": data.get("name"),
        "email": email,
        "subject": data.get("subject"),
        "message": message,
        "status": status,
        "is_read": False,
        "date": datetime.now()
    }

    collection.insert_one(doc)

    return jsonify({"message": "Submitted successfully", "remaining_quota": max(0, 4 - request_count)})


@app.route("/messages", methods=["GET"])
def messages():
    msgs = list(collection.find({}))
    for msg in msgs:
        msg["_id"] = str(msg["_id"])
    return jsonify(msgs)

@app.route("/messages/<msg_id>/read", methods=["POST"])
def mark_read(msg_id):
    try:
        result = collection.update_one({"_id": ObjectId(msg_id)}, {"$set": {"is_read": True}})
        if result.modified_count == 1 or result.matched_count == 1:
            return jsonify({"message": "Message marked as read"}), 200
        else:
            return jsonify({"error": "Message not found"}), 404
    except Exception as e:
        return jsonify({"error": "Invalid ID format"}), 400

@app.route("/messages/<msg_id>/approve", methods=["POST"])
def approve_message(msg_id):
    try:
        result = collection.update_one({"_id": ObjectId(msg_id)}, {"$set": {"status": "Approved"}})
        if result.modified_count == 1 or result.matched_count == 1:
            return jsonify({"message": "Message approved"}), 200
        return jsonify({"error": "Message not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400

@app.route("/messages/<msg_id>/reject", methods=["POST"])
def reject_message(msg_id):
    try:
        result = collection.update_one({"_id": ObjectId(msg_id)}, {"$set": {"status": "Rejected"}})
        if result.modified_count == 1 or result.matched_count == 1:
            return jsonify({"message": "Message rejected"}), 200
        return jsonify({"error": "Message not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400

@app.route("/messages/<msg_id>", methods=["DELETE"])
def delete_message(msg_id):
    try:
        result = collection.delete_one({"_id": ObjectId(msg_id)})
        if result.deleted_count == 1:
            return jsonify({"message": "Message deleted"}), 200
        return jsonify({"error": "Message not found"}), 404
    except:
        return jsonify({"error": "Invalid ID format"}), 400

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user_doc = {
        "name": name,
        "email": email,
        "password_hash": hashed_password.decode('utf-8'),
        "created_at": datetime.now()
    }
    users_collection.insert_one(user_doc)
    return jsonify({"message": "User created successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = users_collection.find_one({"email": email})
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode('utf-8')):
        return jsonify({
            "message": "Login successful", 
            "user": {"name": user.get("name"), "email": email, "avatar": user.get("avatar")}
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/profile", methods=["GET"])
def get_profile():
    # In a real app we'd use JWT tokens. For now, since it's a demo, we fetch the first user
    user = users_collection.find_one({})
    if not user:
        return jsonify({"error": "No users found"}), 404
        
    return jsonify({
        "name": user.get("name", "John Smith"),
        "email": user.get("email", ""),
        "avatar": user.get("avatar", "")
    }), 200

@app.route("/profile", methods=["POST"])
def update_profile():
    data = request.json
    name = data.get("name")
    avatar = data.get("avatar") # Should be a base64 string
    
    # Update the first user in the db for this demo
    user = users_collection.find_one({})
    if not user:
        return jsonify({"error": "No user to update"}), 404
        
    update_data = {}
    if name: update_data["name"] = name
    if avatar is not None: update_data["avatar"] = avatar
    
    users_collection.update_one({"_id": user["_id"]}, {"$set": update_data})
    
    return jsonify({"message": "Profile updated successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
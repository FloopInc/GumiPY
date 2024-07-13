import json
import uuid
import hashlib
import os

STATUS_FILE = 'user/UserStatus.json'

def load_user_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_user_status(user_status):
    with open(STATUS_FILE, 'w') as f:
        json.dump(user_status, f, indent=4)

def is_registered(user_id):
    user_status = load_user_status()
    return str(user_id) in user_status

def register(email, password, user_id):
    if not email or not password:
        return {"message": "Invalid email or password"}

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    filename = str(uuid.uuid4()) + ".json"

    try:
        with open(f"user/auth/{filename}", "w", encoding="utf-8") as json_file:
            json.dump({"email": email, "hashed_password": hashed_password}, json_file, indent=4)

        user_status = load_user_status()
        user_status[str(user_id)] = {"email": email, "filename": filename}
        save_user_status(user_status)

        return {"message": "Account created successfully"}
    except PermissionError as e:
        print(f"Error creating user file: Insufficient permissions. ({e})")
        return {"message": "Registration failed. The bot may lack permissions to create files."}
    except Exception as e:
        print(f"Error creating user file: {e}")
        return {"message": "Registration failed. Please try again later."}

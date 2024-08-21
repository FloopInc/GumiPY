import json
import os

from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

STATUS_FILE = 'user/UserStatus.json'
REGISTER_PASSWORD = "OZMoon"

def load_user_status():
    if os.path.exists(STATUS_FILE):
        with open(STATUS_FILE, 'r') as f:
            data = json.load(f)
            if isinstance(data, dict): 
                return data
    return {}

def save_user_status(user_status):
    with open(STATUS_FILE, 'w') as f:
        json.dump(user_status, f, indent=4)

def is_registered(user_id):
    user_status = load_user_status()
    return user_status.get(str(user_id), {}).get('registered', False)

def unregister(user_id):
    user_status = load_user_status()
    if str(user_id) in user_status:
        user_status[str(user_id)]['registered'] = False
        save_user_status(user_status)
        return {"message": "Unregistration successful. User can no longer use bot commands."}
    return {"message": "User not found."}

def register(user_id, password):
    if password != REGISTER_PASSWORD:
        return {"message": "Invalid password"}

    user_status = load_user_status()

    if not isinstance(user_status, dict):
        return {"message": "Internal error: User status file is corrupted."}

    user_status[str(user_id)] = {"registered": True}
    save_user_status(user_status)

    return {"message": "Registration successful. You can now use all bot commands."}

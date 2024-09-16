import json
import os
from telegram import Update
from telegram.ext import ContextTypes
from handler.register import loadConfig
from handler.event import getEventMessage
from handler.profile import saveUserProfile, loadUserProfile

async def handleBroadcast(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
    user_id = update.message.from_user.id
    user_filepath = f'user/{user_id}.json'
    ownerID = loadConfig()
    
    # Check if user data exists
    if not os.path.exists(user_filepath):
        await update.message.reply_text("User data not found.")
        return

    # Load user data
    with open(user_filepath, 'r') as f:
        user_data = json.load(f)

    # Check if user has item 1010 or enough of item 1000
    if user_data.get("1010", 0) > 0:
        user_data["1010"] -= 1
        if user_data["1010"] <= 0:
            del user_data["1010"]
        saveUserProfile(user_id, user_data)
    elif user_data.get("1000", 0) >= 2499:
        user_data["1000"] -= 2500
        if user_data["1000"] <= 0:
            del user_data["1000"]
        saveUserProfile(user_id, user_data)
    else:
        await update.message.reply_text("Insufficient items or funds to perform the broadcast.")
        return
    
    # Get the username
    username = user_data.get("name", "Unknown User")

    # Load all user statuses
    user_status_filepath = 'data/UserStatus.json'
    with open(user_status_filepath, 'r') as f:
        user_status = json.load(f)

    # Iterate through all users and send message to those with isRadio: true
    broadcast_users = [int(uid) for uid, status in user_status.items() if status.get("isRadio")]

    profileInfo = loadUserProfile(user_id)
    if user_id == ownerID and profileInfo.get('1006', 0) > 0:
        formatted_message = f"**[👑] @Owner Broadcast From KING.`{username}` [👑]**: {message}"
    elif user_id == ownerID:
        formatted_message = f"@Owner Broadcast From @ozmoon1337: {message}" #Change @ozmoon1337 to your username
    elif profileInfo.get('1006', 0) > 0:
        formatted_message = f"**[👑] Super Broadcast From KING.`{username}` [👑]**: {message}"
    else:
        formatted_message = f"Super Broadcast From {username}: {message}"

    event_message = getEventMessage()
    if event_message:
        formatted_message += f"\n\n{event_message}"
    for uid in broadcast_users:
        try:
            await context.bot.send_message(chat_id=uid, text=formatted_message, parse_mode='Markdown')
        except Exception as e:
            print(f"Failed to send message to {uid}: {e}")

    await update.message.reply_text("Broadcast message sent to users.")

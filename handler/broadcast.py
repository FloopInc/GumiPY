import json
import os
from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from handler.register import loadOwner, loadUserProfile, saveUserProfile, getTextMap, isBanned, isRegistered
from handler.event import getEventMessage

async def handleBroadcast(update: Update, context: ContextTypes.DEFAULT_TYPE, message: str):
    user_id = update.message.from_user.id
    user_filepath = f'user/{user_id}.json'
    ownerID = loadOwner()
    
    if not os.path.exists(user_filepath):
        await update.message.reply_text("User data not found.")
        return

    with open(user_filepath, 'r') as f:
        user_data = json.load(f)

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
    
    username = user_data.get("name", "Unknown User")

    user_status_filepath = 'data/UserStatus.json'
    with open(user_status_filepath, 'r') as f:
        user_status = json.load(f)

    broadcast_users = [int(uid) for uid, status in user_status.items() if status.get("isRadio")]

    profileInfo = loadUserProfile(user_id)
    if user_id == ownerID and profileInfo.get('1006', 0) > 0:
        formatted_message = f"**[👑] @Owner Broadcast From KING.`{username}` [👑]**: {message}"
    elif user_id == ownerID:
        formatted_message = f"@Owner Broadcast From @Hanamitsuji: {message}" #Change @Hanamitsuji to your username
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

async def radio_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if isBanned(user_id):
        await update.message.reply_text(isBanned(user_id), parse_mode="Markdown")
        return
    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
    
    user_status_filepath = 'data/UserStatus.json'
    if not os.path.exists(user_status_filepath):
        await update.message.reply_text("User status file not found.")
        return
    
    with open(user_status_filepath, 'r') as f:
        user_status = json.load(f)
    
    user_status[str(user_id)]["isRadio"] = not user_status[str(user_id)].get("isRadio", False)
    
    with open(user_status_filepath, 'w') as f:
        json.dump(user_status, f, indent=4)
    
    current_status = "enabled" if user_status[str(user_id)]["isRadio"] else "disabled"

    if current_status == "enabled":
        msg = getTextMap("radioEnabled")
    else:
        msg = getTextMap("radioDisabled")

    eventMessage = getEventMessage()
    if eventMessage:
        msg += f"\n\n{eventMessage}"
        
    await update.message.reply_text(msg)

from telegram import Update
from telegram.ext import ContextTypes
from handler.profile import inspectProfile, getUserIdFromUsername
from handler.event import getEventMessage
from handler.register import isBanned, isRegistered, getTextMap, loadOwner, loadUserProfile, isMod
import json

with open('data/items.json', 'r') as file:
    items_data = json.load(file)

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()
    ownerID = loadOwner()
    args = message_text.split(" ")
    if isBanned(user_id):
        await update.message.reply_text(isBanned(user_id), parse_mode="Markdown")
        return
    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
    
    if user_id != ownerID and not isMod(user_id) and len(args) > 1:
        await update.message.reply_text(getTextMap("onlyOwner1"))
        return
    
    if len(args) > 1:
        target = args[1]
        if target.startswith("@"):
            # If it's a username, strip the "@" and find the corresponding user_id
            targetUserId = getUserIdFromUsername(target[1:])
            if targetUserId is None:
                await update.message.reply_text(getTextMap("notFound"))
                return
        else:
            targetUserId = target
    else:
        targetUserId = user_id

    profileInfo, targetName = inspectProfile(targetUserId)
    playerInfo = loadUserProfile(targetUserId)

    if not profileInfo:
        await update.message.reply_text(getTextMap("notFound"))
        return
    
        
    if playerInfo.get('1006', 0) > 0:
        profileMessage = f"**[👑]KING.`{targetName}`** Information: \n\n"
    elif user_id == ownerID:
        profileMessage = f"{targetName}'s Information:\n\n"
    elif targetUserId == user_id:
        profileMessage = "Your Information:\n\n"
    
    if targetUserId != user_id:
        profileMessage += f"**[UID]:** {targetUserId}\n\n"

    if isBanned(targetUserId):
        banReason = playerInfo.get('banReason', "Unknown Reason")
        profileMessage += f"**[🚫]Users is Currently Banned** Reason: {banReason}\n\n"


    event_message = getEventMessage()
    if event_message:
        profileMessage += event_message + "\n\n"

    for key, value in profileInfo.items():
        if key != 'name' and key not in items_data:
            profileMessage += f"{key}: {value}\n"

    for item_id, item_data in items_data.items():
        item_name = item_data['name']
        item_logo = item_data['logo']
        item_quantity = profileInfo.get(item_id, 0)
        if item_quantity > 0:
            profileMessage += f"{item_logo} {item_name}: {item_quantity}\n"

    if profileMessage.strip():
        await update.message.reply_text(profileMessage.strip(), parse_mode='Markdown')
    else:
        await update.message.reply_text(getTextMap("errorRequest"))

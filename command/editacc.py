from telegram import Update
from telegram.ext import ContextTypes
from command import dailyquest
from handler.register import loadUserProfile, saveUserProfile, getTextMap
from handler.economy import loadItems
from handler.register import loadOwner
import os

ownerID = loadOwner()

def findUserByName(target_name: str):
    user_dir = 'user/'

    for filename in os.listdir(user_dir):
        if filename.endswith('.json'):
            user_data = loadUserProfile(filename.replace(".json", ""))
            if user_data.get("name", "").lower() == target_name.lower():
                return user_data, filename.replace(".json", "")
    
    return None, None

async def editacc_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    args = context.args

    if user_id != ownerID:
        await update.message.reply_text(getTextMap("onlyOwner"))
        return
    
    if len(args) < 3:
        await update.message.reply_text(getTextMap("editUsage"))
        return

    target_name = args[0]
    action = args[1].lower()
    value = args[2]

    user_data, user_id = findUserByName(target_name)

    if not user_data:
        await update.message.reply_text(getTextMap("notFound"))
        return

    items_data = loadItems()

    if action == "dqid" or action == "dq":
        quest = dailyquest.load_quests()
        if value not in quest:
            await update.message.reply_text(getTextMap("invalidQuestId"))
            return
        user_data["dailyQuestId"] = value
        status_message = f"Updated daily quest ID for {target_name} to {value}."
    elif action == "dqclaim" or action == "dqc":
        if not value.isdigit():
            await update.message.reply_text(getTextMap("valueMustBeNumber"))
            return
        user_data["dailyQuestLastClaim"] = int(value)
        status_message = f"Updated daily quest last claim time for {target_name} to {value}."
    elif action == "dailylogin" or action == "dl":
        if not value.isdigit() or int(value) < 1 or int(value) > 7:
            await update.message.reply_text("Day must be a number between 1 and 7.")
            return
        user_data["dailyLogin"] = int(value)
        status_message = f"Updated daily login for {target_name} to {value}."
    elif action == "dailyclaim" or action == "dlc":
        if not value.isdigit():
            await update.message.reply_text(getTextMap("valueMustBeNumber"))
            return
        user_data["lastClaimTime"] = int(value)
        status_message = f"Updated daily login last claim time for {target_name} to {value}."
    elif action == "clearlogs" or action == "logs":
        user_data["logs"] = []
        status_message = f"Cleared logs for {target_name}."
    else:
        item_id = None
        for key, item in items_data.items():
            if item["name"].lower() == action:
                item_id = key
                break

        if item_id is None:
            await update.message.reply_text(f"Item '{action}' not found in items.")
            return

        try:
            user_data[item_id] = int(value)
            status_message = f"Updated {action} ({items_data[item_id]['logo']}) for {target_name} to {value}."
        except ValueError:
            await update.message.reply_text(getTextMap("valueMustBeNumber"))
            return

    saveUserProfile(user_id, user_data)

    await update.message.reply_text(status_message)

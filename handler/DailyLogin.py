import json, time
from telegram import Update
from telegram.ext import ContextTypes
from handler.economy import loadItems
from handler.event import loadEventData
from handler.register import isBanned, isRegistered, loadUserProfile, saveUserProfile, getTextMap

def loadReward():
    with open('data/DailyReward.json', 'r') as f:
        rewards = json.load(f)
    return rewards

async def dailylogin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()
    args = message_text.split(" ", 1)
    event = loadEventData()
    event_status = event.get("WeeklyLogin", False)

    if isBanned(user_id):
        await update.message.reply_text(isBanned(user_id), parse_mode="Markdown")
        return

    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
    
    if event_status == False:
        await update.message.reply_text('Daily Login Event Not Active')
        return
    
    user_data = loadUserProfile(user_id)
    daily_login = user_data.get("dailyLogin", 0)
    lastClaimTime = user_data.get("lastClaimTime", 0)

    current_time = int(time.time())

    rewards = loadReward()

    items = loadItems()

    if len(args) > 1 and args[1].lower() == "claim":
        if current_time - lastClaimTime < 86400:
            remaining_time = 86400 - (current_time - lastClaimTime)
            remaining_hours = remaining_time // 3600
            remaining_minutes = (remaining_time % 3600) // 60
            await update.message.reply_text(f"⏳ You can claim your daily login rewards again in {remaining_hours} hours and {remaining_minutes} minutes.")
            return
        
        if daily_login >= len(rewards):
            user_data["dailyLogin"] = 1
            user_data["lastClaimTime"] = current_time
            saveUserProfile(user_id, user_data)
            
            current_day = user_data["dailyLogin"]
            reward = rewards[str(current_day)]
            item_id = reward['item_id']
            quantity = reward['quantity']

            item = items.get(item_id)

            if item:
                item_name = item['name']
                item_logo = item['logo']
                user_data[item_id] = user_data.get(item_id, 0) + quantity
                saveUserProfile(user_id, user_data)

                await update.message.reply_text(f"Day 7 Reward Claimed. You received: {item_logo} {item_name} x{quantity} 🎉")
            else:
                await update.message.reply_text("Error: Item not found.")

        else:
            current_day = daily_login + 1
            reward = rewards[str(current_day)] 
            item_id = reward['item_id']
            quantity = reward['quantity']

            item = items.get(item_id)

            if item:
                item_name = item['name']
                item_logo = item['logo']
                user_data[item_id] = user_data.get(item_id, 0) + quantity
                user_data["dailyLogin"] = current_day
                user_data["lastClaimTime"] = current_time
                saveUserProfile(user_id, user_data)

                await update.message.reply_text(f"Day {current_day} reward claimed: {item_logo} {item_name} x{quantity} 🎉")
            else:
                await update.message.reply_text("Error: Item not found.")

        return
    
    response = "🎁 Daily Login Rewards 🎁\n\n"
    for i in range(1, len(rewards) + 1):
        reward = rewards[str(i)]
        item_id = reward['item_id']
        quantity = reward['quantity']

        item = items.get(item_id)
        if item:
            item_name = item['name']
            item_logo = item['logo']
        else:
            item_name = "Unknown Item"
            item_logo = ""

        status = "[CLAIMED]" if i <= daily_login else "[AVAILABLE]"
        response += f"Day {i}: {item_logo} {item_name} x{quantity} {status}\n"

    if daily_login < len(rewards):
        response += f"\nUse `/dailylogin claim` to claim your Day {daily_login + 1} reward."
    else:
        response += "\nUse `/dailylogin claim` to claim your Day 1 reward."

    await update.message.reply_text(response, parse_mode="Markdown")

import json, random, time
from telegram import Update
from telegram.ext import ContextTypes
from handler.economy import loadItems
from handler.register import loadUserProfile, saveUserProfile, isBanned, isRegistered, getTextMap

def load_quests():
    with open('data/DailyQuest.json', 'r') as f:
        return json.load(f)

async def dailyquest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quests = load_quests()
    items = loadItems()
    user_id = update.message.from_user.id
    user_profile = loadUserProfile(user_id)

    if isBanned(user_id):
        await update.message.reply_text(isBanned(user_id), parse_mode='Markdown')
        return
    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
    
    if 'dailyQuestId' in user_profile:
        last_claim_time = user_profile.get('dailyQuestLastClaim', 0)
        current_time = int(time.time())

        if current_time - last_claim_time < 86400:
            remaining_time = 86400 - (current_time - last_claim_time)
            remaining_hours = remaining_time // 3600
            remaining_minutes = (remaining_time % 3600) // 60
            await update.message.reply_text(f"⏳ You have already claimed your quest! Please wait {remaining_hours} hours and {remaining_minutes} minutes before claiming again.")
            return

        today_quest = quests[user_profile['dailyQuestId']]
        
        if not context.args:
            if today_quest['type'] == "Questions":
                await update.message.reply_text(
                    f"📚 >Today's Quest: {today_quest['name']}!< 🌟\n"
                    f"{today_quest['description']}\n\n"
                    f"*Question:* ❓ _{today_quest['questions']}_\n\n"
                    "💬 To complete this quest, answer the question using `/dailyquest <your answer>`",
                parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    f"🚀 *Today's Quest: {today_quest['name']}!* 🌟\n"
                    f"{today_quest['description']}\n\n"
                    "🎁 To complete this quest, you must do `/dailyquest give`.",
                parse_mode='Markdown')
            return 

        action = context.args[0].lower()

        if today_quest['type'] == "Deliver" and action == "give":
            required_items = today_quest['give']
            has_items = all(user_profile.get(item_id, 0) >= quantity for item in required_items for item_id, quantity in item.items())

            if has_items:
                item_names = []
                for item in required_items:
                    for item_id, quantity in item.items():
                        user_profile[item_id] -= quantity
                        item_names.append(f"{items[item_id]['logo']} {items[item_id]['name']} x{quantity}")

                reward_names = []
                for reward in today_quest['reward']:
                    for reward_id, quantity in reward.items():
                        user_profile[reward_id] = user_profile.get(reward_id, 0) + quantity
                        reward_names.append(f"{items[reward_id]['logo']} {items[reward_id]['name']} x{quantity}")

                saveUserProfile(user_id, user_profile)

                await update.message.reply_text(
                    f"🎉 *Congratulations!* You have completed the quest and received:\n" +
                    "\n".join(reward_names),
                    parse_mode='Markdown'
                )

                user_profile['dailyQuestLastClaim'] = int(time.time())
                user_profile.pop('dailyQuestId', None) 
                saveUserProfile(user_id, user_profile)

            else:
                await update.message.reply_text("🚫 You don't have the required items to complete this quest!")

        elif today_quest['type'] == "Questions":
            correct_answer = today_quest['answers'].lower().strip()
            user_answer = ' '.join(context.args).lower().strip()
            
            if user_answer == correct_answer:
                user_profile['dailyQuestLastClaim'] = int(time.time())
                for reward in today_quest['reward']:
                    for reward_id, quantity in reward.items():
                        user_profile[reward_id] = user_profile.get(reward_id, 0) + quantity

                saveUserProfile(user_id, user_profile)
                reward_names = [f"{items[reward_id]['logo']} {items[reward_id]['name']} x{quantity}" for reward in today_quest['reward'] for reward_id, quantity in reward.items()]
                await update.message.reply_text(
                    f"🎉 *Correct answer!* You received the following rewards:\n" +
                    "\n".join(reward_names),
                    parse_mode='Markdown'
                )
                user_profile.pop('dailyQuestId', None)
                saveUserProfile(user_id, user_profile)
            else:
                await update.message.reply_text("❌ That's not the correct answer! Please try again.")



    else:
        quest_id = random.choice(list(quests.keys()))
        today_quest = quests[quest_id]
        user_profile['dailyQuestId'] = quest_id
        saveUserProfile(user_id, user_profile)

        if today_quest['type'] == "Questions":
            await update.message.reply_text(
                f"📚 *Today's Quest: {today_quest['name']}!* 🌟\n"
                f"{today_quest['description']}\n\n"
                f"*Question:* ❓ _{today_quest['questions']}_\n\n"
                "💬 To complete this quest, answer the question using `/dailyquest <your answer>`",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                f"🚀 *Today's Quest: {today_quest['name']}!* 🌟\n"
                f"{today_quest['description']}\n\n"
                "🎁 To complete this quest, you must do `/dailyquest give`.",
                parse_mode='Markdown'
            )

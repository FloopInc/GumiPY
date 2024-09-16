from telegram import Update
from telegram.ext import CallbackContext
from handler.event import toggleCrownDay, toggleBroadcastDay
from handler import register

async def event_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    isBanned = register.isBanned(user_id)
    registered = register.isRegistered(user_id)
    ownerId = register.loadConfig()
    TextMap = register.loadTextMap()

    if not ownerId == user_id:
        await update.message.reply_text(TextMap["onlyOwner"])
        return
        
    if isBanned:
        await update.message.reply_text(TextMap["isBanned"])
        return

    if not registered:
        await update.message.reply_text(TextMap["notRegistered"])
        return
    
    args = context.args

    if len(args) == 0:
        await update.message.reply_text("Please specify an event name. Example: /event CrownDay")
        return
    
    event_name = args[0].lower()

    if event_name == "crown":
        result = toggleCrownDay()
        if result["status"]:
            await update.message.reply_text("CrownDay event is now active! Crown Title is now tradeable.")
        else:
            await update.message.reply_text("CrownDay event is now inactive! Crown Title is back to being untradeable.")
        return
    elif event_name == "broadcast":
        result = toggleBroadcastDay()
        if result["status"]:
            await update.message.reply_text("BroadcastDay event is now active! Megaphone is now tradeable.")
        else:
            await update.message.reply_text("BroadcastDay event is now inactive! Megaphone is back to being untradeable.")
        return

    await update.message.reply_text(f"Event '{event_name}' not found.")

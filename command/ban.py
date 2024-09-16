from telegram import Update
from telegram.ext import ContextTypes

from handler.register import isBanned, ban, getTextMap, loadConfig

async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()
    ownerID = loadConfig()
    args = message_text.split(" ")
    
    if isBanned(update.message.from_user.id):
        await update.message.reply_text(getTextMap("userBanned"))
        return
    
    if not ownerID == user_id:
        await update.message.reply_text(getTextMap("onlyOwner"))
        return
    
    if len(args) == 1:
        await update.message.reply_text(getTextMap("notFound"))
        return

    targetUserId = args[1]

    result = ban(targetUserId)
    await update.message.reply_text(result["message"])
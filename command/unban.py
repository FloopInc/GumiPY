from telegram import Update
from telegram.ext import ContextTypes

from handler.register import isBanned, unban, getTextMap, loadConfig
async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()
    ownerID = loadConfig()
    args = message_text.split(" ")
    
    if not ownerID == user_id:
        await update.message.reply_text(getTextMap("onlyOwner"))
        return
    
    if isBanned(update.message.from_user.id):
        await update.message.reply_text(getTextMap("userBanned"))
        return
    
    if len(args) == 1:
        await update.message.reply_text(getTextMap("notFound"))
        return

    targetUserId = args[1]

    result = unban(targetUserId)
    await update.message.reply_text(result["message"])
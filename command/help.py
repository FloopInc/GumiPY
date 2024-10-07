from telegram import Update
from telegram.ext import ContextTypes

from handler.register import isRegistered, isBanned, getTextMap
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if isBanned(user_id):
        await update.message.reply_text(isBanned(user_id), parse_mode="Markdown")
        return
    
    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return

    await update.message.reply_text("This is the help message.")

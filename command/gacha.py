from telegram import Update
from telegram.ext import ContextTypes
from handler.economy import performGacha
from handler.register import isRegistered, isBanned, getTextMap
from handler.event import getEventMessage 

async def gacha_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    args = context.args
    
    if isBanned(user_id):
        await update.message.reply_text(isBanned(user_id), parse_mode="Markdown")
        return
    
    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
    
    boxIdOrName = " ".join(args)
    
    result = performGacha(user_id, boxIdOrName)
    final_message = result["message"]

    event_message = getEventMessage()
    if event_message:
        final_message += f"\n\n{event_message}"

    await update.message.reply_text(final_message)

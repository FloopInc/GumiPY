from telegram import Update
from telegram.ext import ContextTypes
from handler.event import getEventMessage
from handler.register import isBanned, isRegistered, loadConfig, getTextMap
from handler.economy import giveItem, modGiveItem

ownerID = loadConfig()
async def give_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    args = context.args
    if isBanned(user_id):
        await update.message.reply_text(getTextMap("isBanned"))
        return
    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
        
    if len(args) < 3:
        await update.message.reply_text(getTextMap("giveUsage"))
        return
    
    toUserName = args[0]
    item_name = " ".join(args[1:-1])
    quantity = int(args[-1])
    
    if user_id == ownerID:
        result = modGiveItem(user_id, toUserName, item_name, quantity)
    else:
        result = giveItem(user_id, toUserName, item_name, quantity)
    
    # await update.message.reply_text(result["message"])
    final_message = result["message"]

    event_message = getEventMessage()
    if event_message:
        final_message += f"\n\n{event_message}"

    await update.message.reply_text(final_message)

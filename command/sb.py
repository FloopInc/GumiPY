from telegram import Update
from telegram.ext import CallbackContext
from handler.broadcast import handleBroadcast
from handler.register import isRegistered, isBanned, getTextMap

async def sb_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    args = context.args
    
    if isBanned(user_id):
        await update.message.reply_text(getTextMap("isBanned"))
        return
    
    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
    
    if not args:
        await update.message.reply_text("Please provide a message to broadcast.")
        return
    
    message = " ".join(context.args)

    # Call handle_broadcast
    await handleBroadcast(update, context, message)

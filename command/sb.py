from telegram import Update
from telegram.ext import CallbackContext
from handler.broadcast import handleBroadcast
from handler.register import isRegistered, isBanned, getTextMap
import time, colorama

async def sb_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    args = context.args
    
    
    if isBanned(user_id):
        await update.message.reply_text(isBanned(user_id), parse_mode="Markdown")
        return
    
    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
    
    if not args:
        await update.message.reply_text("Please provide a message to broadcast.")
        return
    
    message = " ".join(context.args)

    await handleBroadcast(update, context, message)
    print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] Broadcast From {user_id}/{update.message.from_user.username}: {message}")

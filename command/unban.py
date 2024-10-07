from telegram import Update
from telegram.ext import ContextTypes

from handler.register import isBanned, unban, getTextMap, loadOwner, loadUserStatus

async def unban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()
    ownerID = loadOwner()
    args = message_text.split(" ", 2)

    if not ownerID == user_id:
        await update.message.reply_text(getTextMap("onlyOwner"))
        return

    if isBanned(update.message.from_user.id):
        await update.message.reply_text(getTextMap("userBanned"))
        return

    if len(args) < 2:
        await update.message.reply_text(getTextMap("notFound"))
        return

    target = args[1]
    unban_reason = args[2] if len(args) > 2 else "No reason provided"

    user_status = loadUserStatus()

    if target.isdigit() and target in user_status:
        target_user_id = target
    else:
        target_user_id = None
        for user_id, user_info in user_status.items():
            if user_info.get("username", "").lower() == target.lower():
                target_user_id = user_id
                break

    if target_user_id:
        result = unban(target_user_id, unban_reason)
        await update.message.reply_text(result["message"])
    else:
        await update.message.reply_text(getTextMap("notFound"))

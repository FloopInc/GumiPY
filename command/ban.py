from telegram import Update
from telegram.ext import ContextTypes
from handler.register import isBanned, ban, getTextMap, loadOwner, loadUserStatus
import time,colorama
def convertTime(time_str):
    unit = time_str[-1].lower()
    value = int(time_str[:-1])
    if unit == 's':
        return value
    elif unit == 'm':
        return value * 60
    elif unit == 'h':
        return value * 3600
    elif unit == 'd':
        return value * 86400
    else:
        raise ValueError("Invalid time format")

async def ban_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()
    ownerID = loadOwner()
    args = message_text.split(" ", 3)
    user_status = loadUserStatus()

    if not ownerID == user_id:
        await update.message.reply_text(getTextMap("onlyOwner"))
        return
    
    if len(args) < 3:
        await update.message.reply_text("Usage: /ban <username> <time> <reason>")
        return

    target = args[1]
    action_time = args[2]
    ban_reason = args[3] if len(args) > 3 else "No reason provided"

    try:
        ban_duration = convertTime(action_time)
    except ValueError:
        await update.message.reply_text("Invalid time format! Use s/m/h/d.")
        return

    if target.isdigit() and target in user_status:
        targetUserId = target
    else:
        targetUserId = None
        for user_id, user_info in user_status.items():
            if user_info.get("username", "").lower() == target.lower():
                targetUserId = user_id
                break

    if targetUserId == user_id:
        await update.message.reply_text("You can't ban yourself!")
        return
    
    if isBanned(targetUserId):
        await update.message.reply_text(getTextMap("alrBanned"))
        return

    if targetUserId:
        result = ban(targetUserId, ban_reason, ban_duration)
        print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{colorama.Fore.RED}BANNED{colorama.Style.RESET_ALL}] {update.message.from_user.username} banned {targetUserId} for {action_time}. Reason: ({ban_reason})")
        await update.message.reply_text(result["message"])

        target_user_info = user_status.get(targetUserId)
        target_username = target_user_info.get("username", "Unknown User") if target_user_info else "Unknown User"

        allUsers = [int(uid) for uid, status in user_status.items()]
        for uid in allUsers:
            try:
                await context.bot.send_message(chat_id=uid, text=f'**The Ancient ones have** `banned` @{target_username} **(`/rules` to see the rules!)**', parse_mode="Markdown")
            except Exception as e:
                print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{colorama.Fore.RED}ERROR{colorama.Style.RESET_ALL}] Failed to send message to {uid}: {e}")
    else:
        await update.message.reply_text(getTextMap("notFound"))

from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import json,os,time,psutil,sys
from command import sourcecode, help, start, check, ban, unban, hotfix, info, gacha, give,store,event,sb,mods
from handler.event import getEventMessage
from handler.register import register, unregister, isRegistered, isBanned, getTextMap, loadConfig

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
with open('data/config.json') as config_file:
    config_data = json.load(config_file)
    botToken = config_data["TOKEN"]
    botUsername = config_data["username"]
TOKEN: Final = botToken
BOT_USERNAME: Final = botUsername
ownerID = loadConfig()

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Halo juga ada yg bisa dibanting?'

    return 'I am sorry, I do not understand.'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"Received message from user ({update.message.chat.id}) in {message_type}: {text}")

    
async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    ownerID = loadConfig()

    if isBanned(user_id):
        await update.message.reply_text(getTextMap("isBanned"))
        return
    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
    
    # Calculate response time
    start_time = time.time()
    await update.message.reply_text("Requesting...")  
    end_time = time.time()
    ping_time = int((end_time - start_time) * 1000)  

    if user_id == ownerID:
        # Memory usage
        memory_info = psutil.virtual_memory()
        total_memory = memory_info.total // (1024 * 1024)
        used_memory = memory_info.used // (1024 * 1024)
        memory_message = f"Memory Usage: {used_memory}MB/{total_memory}MB"

        # CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_message = f"CPU Usage: {cpu_usage}%"

        # Uptime
        bootTimestamp = psutil.boot_time()
        uptime_seconds = time.time() - bootTimestamp
        uptime_message = f"Uptime: {int(uptime_seconds // 3600)}h {int((uptime_seconds % 3600) // 60)}m"

        user_folder = 'user/'
        total_users = len([name for name in os.listdir(user_folder) if os.path.isfile(os.path.join(user_folder, name))])
        user_message = f"Total Registered Users: {total_users}"

        response = f"Server Status:\n\nPing: ({ping_time} ms)\n{memory_message}\n{cpu_message}\n{uptime_message}\n{user_message}"
    else:
        response = f"Pong! ({ping_time} ms)"

    eventMessage = getEventMessage()
    if eventMessage:
        response += f"\n\n{eventMessage}"

    await update.message.reply_text(response)

async def radio_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if isBanned(user_id):
        await update.message.reply_text(getTextMap("isBanned"))
        return
    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
    
    user_status_filepath = 'data/UserStatus.json'
    if not os.path.exists(user_status_filepath):
        await update.message.reply_text("User status file not found.")
        return
    
    with open(user_status_filepath, 'r') as f:
        user_status = json.load(f)
    
    user_status[str(user_id)]["isRadio"] = not user_status[str(user_id)].get("isRadio", False)
    
    # Save updated status
    with open(user_status_filepath, 'w') as f:
        json.dump(user_status, f, indent=4)
    
    current_status = "enabled" if user_status[str(user_id)]["isRadio"] else "disabled"

    if current_status == "enabled":
        msg = getTextMap("radioEnabled")
    else:
        msg = getTextMap("radioDisabled")

    eventMessage = getEventMessage()
    if eventMessage:
        msg += f"\n\n{eventMessage}"
        
    await update.message.reply_text(msg)

async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()
    password = message_text.split(" ")[1] if len(message_text.split(" ")) > 1 else None

    if isBanned(user_id):
        await update.message.reply_text(getTextMap("isBanned"))
        return
    
    if isRegistered(user_id):
        await update.message.reply_text(getTextMap("registered"))
        return
    
    registration_response = register(user_id, password)
    await update.message.reply_text(registration_response["message"])

async def unregister_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()
    args = message_text.split(" ")

    if not ownerID == user_id:
        await update.message.reply_text(getTextMap("onlyOwner"))
        return
    
    if len(args) == 1:
        await update.message.reply_text(getTextMap("notFound"))
        return

    targetUserId = args[1]

    try:
        if targetUserId == str(user_id):
            result = unregister(user_id)
            await update.message.reply_text(result["message"])
        else:
            if not isRegistered(targetUserId):
                await update.message.reply_text(getTextMap("notFound"))
                return

            result = unregister(targetUserId)
            await update.message.reply_text(result["message"])
    except Exception as e:
        print(f"Error during unregister command: {e}")
        await update.message.reply_text(getTextMap("errorRequest"))

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start.start_command))
    app.add_handler(CommandHandler("help", help.help_command))
    app.add_handler(CommandHandler("sourcecode", sourcecode.sourcecode_command))
    app.add_handler(CommandHandler("check", check.check_version))
    app.add_handler(CommandHandler("ban", ban.ban_command))
    app.add_handler(CommandHandler("unban", unban.unban_command))
    app.add_handler(CommandHandler("hotfix", hotfix.hotfix_command))
    app.add_handler(CommandHandler("info", info.info_command))
    app.add_handler(CommandHandler("gacha", gacha.gacha_command))
    app.add_handler(CommandHandler("give", give.give_command))
    app.add_handler(CommandHandler("store", store.store_command))
    app.add_handler(CommandHandler("event", event.event_command))
    app.add_handler(CommandHandler("sb", sb.sb_command))
    app.add_handler(CommandHandler("mods", mods.mods_command))
    
    app.add_handler(CommandHandler("radio", radio_command))
    app.add_handler(CommandHandler("ping", ping_command))
    app.add_handler(CommandHandler("register", register_command))
    app.add_handler(CommandHandler("unregister", unregister_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)
    print('Polling bot...')
    app.run_polling(poll_interval=5)

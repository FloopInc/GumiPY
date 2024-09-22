from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, CallbackContext
import json,os,time,psutil,tempfile
from command import help, start, check, ban, unban, hotfix, info, gacha, give,store,event,sb,mods 
from handler.broadcast import radio_command
from handler.event import getEventMessage
from handler.register import isRegistered, isBanned, getTextMap, loadConfig, register_command
from PIL import Image
from rembg import remove

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
        return 'Hello there ! How can I help you today ? contact moderators for help /mods'

    return 'I am sorry, I do not understand.'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"Received message from user ({update.message.chat.id}) in {message_type}: {text}")
    if message_type == 'group':
        if not isRegistered(update.message.from_user.id):
            await update.message.reply_text(getTextMap("notRegistered"))
            return
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        if not isRegistered(update.message.from_user.id):
            await update.message.reply_text(getTextMap("notRegistered"))
            return
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)
    
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

def remove_background(input_image_path, output_image_path):
    input_image = Image.open(input_image_path)
    output_image = remove(input_image)
    output_image.save(output_image_path)

async def removebg_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await context.bot.get_file(photo.file_id)
    
    with tempfile.TemporaryDirectory() as tmpdirname:
        input_image_path = os.path.join(tmpdirname, 'input_image.png')
        output_image_path = os.path.join(tmpdirname, 'output_image.png')

        await file.download_to_drive(input_image_path)

        remove_background(input_image_path, output_image_path)

        with open(output_image_path, 'rb') as output_image_file:
            await update.message.reply_photo(photo=output_image_file)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start.start_command))
    app.add_handler(CommandHandler("help", help.help_command))
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
    app.add_handler(MessageHandler(filters.PHOTO, removebg_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)
    print('Polling bot...')
    app.run_polling(poll_interval=5)

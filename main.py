from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import json,os,time,psutil,tempfile
from command import setacc, editacc, help, start, check, ban, unban, hotfix, info, gacha, give,store,sb,mods,redeemcode,dailyquest,search
from handler.broadcast import radio_command
from handler.event import getEventMessage, event_command
from handler.DailyLogin import dailylogin_command
from handler.register import isRegistered, isBanned, getTextMap, loadOwner, register_command
from handler import textmap
from colorama import Fore, Style
from PIL import Image
from rembg import remove

with open('data/config.json') as config_file:
    config_data = json.load(config_file)
    botToken = config_data["TOKEN"]
    botUsername = config_data["username"]
TOKEN: Final = botToken
BOT_USERNAME: Final = botUsername

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hello there ! How can I help you today ? contact moderators for help /mods'

    return 'I am sorry, I do not understand.'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{Fore.YELLOW}MESSAGE{Style.RESET_ALL}] Received message from user ({update.message.chat.id}) in {message_type}: {text}")
    if message_type == 'group':
        if isBanned(update.message.from_user.id):
            await update.message.reply_text(isBanned(update.message.from_user.id), parse_mode="Markdown")
            return
        if not isRegistered(update.message.from_user.id):
            await update.message.reply_text(getTextMap("notRegistered"))
            return
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        if isBanned(update.message.from_user.id):
            await update.message.reply_text(isBanned(update.message.from_user.id), parse_mode="Markdown")
            return
        if not isRegistered(update.message.from_user.id):
            await update.message.reply_text(getTextMap("notRegistered"))
            return
        response: str = handle_response(text)

    print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{Fore.GREEN}BOT{Style.RESET_ALL}] Response:", response)
    await update.message.reply_text(response)
    
async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    ownerID = loadOwner()

    if isBanned(user_id):
        await update.message.reply_text(isBanned(user_id), parse_mode="Markdown")
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
        response = f"Pong! ({ping_time} ms) \n{uptime_message}"

    eventMessage = getEventMessage()
    if eventMessage:
        response += f"\n\n{eventMessage}"

    await update.message.reply_text(response)
async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open('rules.txt', 'r') as file:
        rules_text = file.read()
    await update.message.reply_text(rules_text, parse_mode="Markdown")


def remove_background(input_image_path, output_image_path):
    input_image = Image.open(input_image_path)
    output_image = remove(input_image)
    output_image.save(output_image_path)

async def removebg_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if isBanned(user_id):
        await update.message.reply_text(isBanned(user_id), parse_mode="Markdown")
        return

    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
    
    await update.message.reply_text("Please upload an image, and I'll remove the background!")

    context.user_data[user_id] = "waiting_for_image"

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if context.user_data.get(user_id) == "waiting_for_image":
        await update.message.reply_text("Processing your image... This might take a few seconds.")

        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)

        with tempfile.TemporaryDirectory() as tmpdirname:
            input_image_path = os.path.join(tmpdirname, 'input_image.png')
            output_image_path = os.path.join(tmpdirname, 'output_image.png')

            await file.download_to_drive(input_image_path)

            try:
                remove_background(input_image_path, output_image_path)

                with open(output_image_path, 'rb') as output_image_file:
                    await update.message.reply_photo(photo=output_image_file)

                await update.message.reply_text("Done! Here's your image with the background removed.")

            except Exception as e:
                await update.message.reply_text(getTextMap('errorRequest') + str(e))

        context.user_data[user_id] = None

    else:
        await update.message.reply_text("Please run /removebg first and then upload an image.")

def cleanup_tempfiles(max_age=3600):
    temp_dir = tempfile.gettempdir()
    current_time = time.time()
    
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        
        if os.path.isfile(file_path) and filename.endswith('.json'):
            file_age = current_time - os.path.getmtime(file_path)
            
            if file_age > max_age:
                os.remove(file_path)
                print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{Fore.BLUE}INFO{Style.RESET_ALL}] Deleted temporary file: {file_path}")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{Fore.BLUE}INFO{Style.RESET_ALL}] Starting bot...")
    app = Application.builder().token(TOKEN).build()
    cleanup_tempfiles()

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
    app.add_handler(CommandHandler("sb", sb.sb_command))
    app.add_handler(CommandHandler("mods", mods.mods_command))
    app.add_handler(CommandHandler("setacc", setacc.setacc_command))
    app.add_handler(CommandHandler("editacc", editacc.editacc_command))
    app.add_handler(CommandHandler("redeemcode", redeemcode.redeemcode_command))
    app.add_handler(CommandHandler("textmapdiff", textmap.textmapdiff_command))
    app.add_handler(CommandHandler("dailyquest", dailyquest.dailyquest_command))
    
    app.add_handler(CommandHandler("event", event_command))
    app.add_handler(CommandHandler("rules", rules_command))
    app.add_handler(CommandHandler("radio", radio_command))
    app.add_handler(CommandHandler("dailylogin", dailylogin_command))
    app.add_handler(CommandHandler("ping", ping_command))
    app.add_handler(CommandHandler("search", search.search_command))
    app.add_handler(CommandHandler("register", register_command))
    app.add_handler(CommandHandler("removebg", removebg_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^https?://'), textmap.handle_url))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{Fore.BLUE}INFO{Style.RESET_ALL}] Loading data files...")
    app.add_error_handler(error)
    data_files = {
    "items.json": ("items_data", "Item IDs"),
    "Event.json": ("event_data", "Event IDs"),
    "dispatch.json": ("dispatch_data", "Dispatch Links"),
    "DailyQuest.json": ("dailyquest_data", "Daily Quest"),
    "UserStatus.json": ("userstatus_data", "User Status"),
    "TextMap.json": ("textmap_data", "TextMap")
    }

    for file in os.listdir("data"):
        if file.endswith(".json") and not file.startswith("_"):
            print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{Fore.BLUE}INFO{Style.RESET_ALL}] Loading data file: {file}")
        
        if file in data_files:
            var_name, description = data_files[file]
            with open(f'data/{file}', 'r') as f:
                globals()[var_name] = json.load(f)
                print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{Fore.BLUE}INFO{Style.RESET_ALL}] Loaded {len(globals()[var_name])} {description}")
    print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{Fore.BLUE}INFO{Style.RESET_ALL}] Polling bot...")
    print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{Fore.RED}WARN{Style.RESET_ALL}] GUMIPY IS A FREE SOFTWARE & OPEN SOURCE. DO NOT SELL! IF YOU PAID FOR IT, YOU HAVE BEEN SCAMMED!")
    app.run_polling(poll_interval=5)
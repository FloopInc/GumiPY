from telegram import Update
from telegram.ext import ContextTypes
from handler.event import getEventMessage
from handler.economy import usercd
from handler.register import isRegistered, isBanned, loadUserStatus, getTextMap, loadUserProfile, userStats
import time
from colorama import Fore, Style

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    userStatus = loadUserStatus()
    userProfile = loadUserProfile(user_id)
    name = update.message.from_user.first_name
    
    if str(user_id) not in userProfile:
        usercd(user_id, name)

    if str(user_id) not in userStatus:
        userStats(user_id, username)
        print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{Fore.BLUE}INFO{Style.RESET_ALL}] User {user_id}/{username} started bot.")
        await update.message.reply_text(getTextMap("welcomeUnregistered"))
    else:
        if isBanned(user_id):
            await update.message.reply_text(isBanned(user_id), parse_mode="Markdown")
            return
        
        if not isRegistered(user_id):
            await update.message.reply_text(getTextMap("notRegistered"))
            return
        
        welcome_message = f"Welcome, {name}! To get started, type /help."

        event_message = getEventMessage()
        if event_message:
            welcome_message += f"\n\n{event_message}"

        await update.message.reply_text(welcome_message)


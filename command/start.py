from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

from auth.register import register, is_registered
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if not is_registered(user_id):
        await update.message.reply_text("You are not registered. Please register using /register <password>.")
    else:
        await update.message.reply_text(f"Welcome back, {update.message.from_user.first_name}!")

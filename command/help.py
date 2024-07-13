from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

from auth.register import register, is_registered
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_registered(update.message.from_user.id):
        await update.message.reply_text("You are not registered. Please register using /register <email> <password>.")
        return

    await update.message.reply_text("This is the help message.")

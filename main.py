from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

import json

from command import help, start
from auth.register import register, unregister, is_registered

with open('config.json') as config_file:
    config_data = json.load(config_file)
    botToken = config_data["TOKEN"]
    botUsername = config_data["username"]
TOKEN: Final = botToken
BOT_USERNAME: Final = botUsername

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Halo juga ada yg bisa dibanting?'

    return 'I am sorry, I do not understand.'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"Received message from user ({update.message.chat.id}) in {message_type}: {text}")


async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()
    password = message_text.split(" ")[1] if len(message_text.split(" ")) > 1 else None

    if is_registered(user_id):
        await update.message.reply_text("Hey, You are already registered! You dont have to use /register command again, Type /help for a list of commands")
        return
    
    registration_response = register(user_id, password)
    await update.message.reply_text(registration_response["message"])

async def unregister_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()
    args = message_text.split(" ")

    
    if len(args) == 1:
        await update.message.reply_text("Please provide a user ID to unregister.")
        return

    target_user_id = args[1]

    try:
        if target_user_id == str(user_id):
            result = unregister(user_id)
            await update.message.reply_text(result["message"])
        else:
            if not is_registered(target_user_id):
                await update.message.reply_text("User ID not found or not registered.")
                return

            result = unregister(target_user_id)
            await update.message.reply_text(result["message"])
    except Exception as e:
        print(f"Error during unregister command: {e}")
        await update.message.reply_text("An error occurred while processing your request. Please try again later.")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start.start_command))
    app.add_handler(CommandHandler("help", help.help_command))

    app.add_handler(CommandHandler("register", register_command))
    app.add_handler(CommandHandler("unregister", unregister_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)
    print('Polling bot...')
    app.run_polling(poll_interval=5)

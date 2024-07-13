from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from command import help, start
from auth.register import register

TOKEN: Final = ""
BOT_USERNAME: Final = "Narita Tsugumi"

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
    message_text = update.message.text
    arguments = message_text.split()[1:]

    if len(arguments) != 2:
        await update.message.reply_text("Invalid format. Please use: /register <email> <password>")
        return

    email = arguments[0]
    password = arguments[1]

    print(f"Calling register function with email: {email}, password: {password}")

    # Call the register function
    registration_response = register(email, password)

    # Debugging: Print the response
    print(f"Registration response: {registration_response}")

    await update.message.reply_text(registration_response["message"])

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == "__main__":
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start.start_command))
    app.add_handler(CommandHandler("help", help.help_command))

    app.add_handler(CommandHandler("register", register_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.add_error_handler(error)
    print('Polling bot...')
    app.run_polling(poll_interval=5)

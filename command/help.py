from telegram import Update
from telegram.ext import ContextTypes
from auth.register import is_registered,is_banned
async def help_command(update,context):
	A=update;B=A.message.from_user.id
	if is_banned(B):await A.message.reply_text('Sorry, but you have been banned from using this bot. If you believe this is a mistake, please contact support @ozmoon1337.');return
	if not is_registered(B):await A.message.reply_text('You are not registered. Please register using /register <password>.');return
	await A.message.reply_text('This is the help message.')
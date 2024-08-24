from telegram import Update
from telegram.ext import ContextTypes
from auth.economy import usercd
from auth.register import is_registered,is_banned,load_user_status,save_user_status
async def start_command(update,context):
	D=False;A=update;B=A.message.from_user.id;C=load_user_status();E=A.message.from_user.first_name;usercd(B,E)
	if str(B)not in C:C[str(B)]={'registered':D,'isBanned':D};save_user_status(C);await A.message.reply_text('Welcome to the bot. Please register using /register <password>.')
	else:
		if is_banned(B):await A.message.reply_text('Sorry, but you have been banned from using this bot. If you believe this is a mistake, please contact support @ozmoon1337.');return
		if not is_registered(B):await A.message.reply_text('You are not registered. Please register using /register <password>.');return
		await A.message.reply_text(f"Welcome back, {A.message.from_user.first_name}!")
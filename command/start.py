from telegram import Update
from telegram.ext import ContextTypes
from auth.economy import usercd
from handler.register import isRegistered,isBanned,loadUserStatus,saveUserStatus,getTextMap
async def start_command(update,context):
	F=False;E='isBanned';A=update;B=A.message.from_user.id;C=loadUserStatus();D=A.message.from_user.first_name;usercd(B,D)
	if str(B)not in C:C[str(B)]={'registered':F,E:F};saveUserStatus(C);await A.message.reply_text(getTextMap('welcomeUnregistered'))
	else:
		if isBanned(B):await A.message.reply_text(getTextMap(E));return
		if not isRegistered(B):await A.message.reply_text(getTextMap('notRegistered'));return
		await A.message.reply_text(f"Welcome, {D}! to get started, type /help.")
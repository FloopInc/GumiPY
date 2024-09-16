from telegram import Update
from telegram.ext import ContextTypes
from handler.event import getEventMessage
from handler.economy import usercd
from handler.register import isRegistered,isBanned,loadUserStatus,saveUserStatus,getTextMap
async def start_command(update,context):
	H='isBanned';C=False;A=update;B=A.message.from_user.id;I=A.message.from_user.username;D=loadUserStatus();E=A.message.from_user.first_name;usercd(B,E)
	if str(B)not in D:D[str(B)]={'username':I,'registered':C,H:C,'isModerator':C,'isHidden':C,'isRadio':True};saveUserStatus(D);await A.message.reply_text(getTextMap('welcomeUnregistered'))
	else:
		if isBanned(B):await A.message.reply_text(getTextMap(H));return
		if not isRegistered(B):await A.message.reply_text(getTextMap('notRegistered'));return
		F=f"Welcome, {E}! To get started, type /help.";G=getEventMessage()
		if G:F+=f"\n\n{G}"
		await A.message.reply_text(F)
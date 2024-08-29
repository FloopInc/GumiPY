from telegram import Update
from telegram.ext import ContextTypes
from handler.register import isRegistered,isBanned,getTextMap
async def help_command(update,context):
	A=update;B=A.message.from_user.id
	if isBanned(B):await A.message.reply_text(getTextMap('isBanned'));return
	if not isRegistered(B):await A.message.reply_text(getTextMap('notRegistered'));return
	await A.message.reply_text('This is the help message.')
from telegram import Update
from telegram.ext import ContextTypes
from auth.economy import performGacha
from handler.register import isRegistered,isBanned,getTextMap
async def gacha_command(update,context):
	A=update;B=A.message.from_user.id;C=context.args
	if isBanned(B):await A.message.reply_text(getTextMap('isBanned'));return
	if not isRegistered(B):await A.message.reply_text(getTextMap('notRegistered'));return
	D=' '.join(C);E=performGacha(B,D);await A.message.reply_text(E['message'])
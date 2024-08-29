from telegram import Update
from telegram.ext import ContextTypes
from handler.register import isBanned,ban,getTextMap,loadConfig
async def ban_command(update,context):
	A=update;C=A.message.from_user.id;D=A.message.text.strip();E=loadConfig();B=D.split(' ')
	if isBanned(A.message.from_user.id):await A.message.reply_text(getTextMap('userBanned'));return
	if not E==C:await A.message.reply_text(getTextMap('onlyOwner'));return
	if len(B)==1:await A.message.reply_text(getTextMap('notFound'));return
	F=B[1];G=ban(F);await A.message.reply_text(G['message'])
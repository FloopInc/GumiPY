from telegram import Update
from telegram.ext import ContextTypes
from handler.register import isBanned,unban,getTextMap,loadConfig
async def unban_command(update,context):
	A=update;C=A.message.from_user.id;D=A.message.text.strip();E=loadConfig();B=D.split(' ')
	if not E==C:await A.message.reply_text(getTextMap('onlyOwner'));return
	if isBanned(A.message.from_user.id):await A.message.reply_text(getTextMap('userBanned'));return
	if len(B)==1:await A.message.reply_text(getTextMap('notFound'));return
	F=B[1];G=unban(F);await A.message.reply_text(G['message'])
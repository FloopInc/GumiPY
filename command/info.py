from telegram import Update
from telegram.ext import ContextTypes
from handler.profile import inspectProfile,loadUserProfile
from handler.register import isBanned,isRegistered,getTextMap,loadConfig,isMod
import json
with open('data/items.json','r')as file:items_data=json.load(file)
async def info_command(update,context):
	K='name';A=update;C=A.message.from_user.id;L=A.message.text.strip();M=loadConfig();G=L.split(' ')
	if isBanned(C):await A.message.reply_text(getTextMap('isBanned'));return
	if not isRegistered(C):await A.message.reply_text(getTextMap('notRegistered'));return
	if C!=M and not isMod(C)and len(G)>1:await A.message.reply_text(getTextMap('onlyOwner1'));return
	if len(G)>1:D=G[1]
	else:D=C
	E,H=inspectProfile(D);N=loadUserProfile(D)
	if not E:await A.message.reply_text(getTextMap('notFound'));return
	if N.get('1006',0)>0:B=f"**[👑]KING.`{H}`** Information: \n\n"
	elif D==C:B='Your Information:\n\n'
	elif C==M:B=f"{H}'s Information:\n\n"
	else:await A.message.reply_text(getTextMap('onlyOwner1'));return
	for(F,O)in E.items():
		if F!=K and F not in items_data:B+=f"{F}: {O}\n"
	for(P,I)in items_data.items():
		Q=I[K];R=I['logo'];J=E.get(P,0)
		if J>0:B+=f"{R} {Q}: {J}\n"
	if B.strip():await A.message.reply_text(B.strip(),parse_mode='Markdown')
	else:await A.message.reply_text(getTextMap('errorRequest'))

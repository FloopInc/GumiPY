from telegram import Update
from telegram.ext import ContextTypes
from handler.profile import inspectProfile,getUserIdFromUsername
from handler.event import getEventMessage
from handler.register import isBanned,isRegistered,getTextMap,loadOwner,loadUserProfile,isMod
import json
with open('data/items.json','r')as file:items_data=json.load(file)
async def info_command(update,context):
	Q='name';P='notFound';O='Markdown';A=update;B=A.message.from_user.id;R=A.message.text.strip();I=loadOwner();E=R.split(' ')
	if isBanned(B):await A.message.reply_text(isBanned(B),parse_mode=O);return
	if not isRegistered(B):await A.message.reply_text(getTextMap('notRegistered'));return
	if B!=I and not isMod(B)and len(E)>1:await A.message.reply_text(getTextMap('onlyOwner1'));return
	if len(E)>1:
		F=E[1]
		if F.startswith('@'):
			C=getUserIdFromUsername(F[1:])
			if C is None:await A.message.reply_text(getTextMap(P));return
		else:C=F
	else:C=B
	G,J=inspectProfile(C);K=loadUserProfile(C)
	if not G:await A.message.reply_text(getTextMap(P));return
	if K.get('1006',0)>0:D=f"**[👑]KING.`{J}`** Information: \n\n"
	elif B==I:D=f"{J}'s Information:\n\n"
	elif C==B:D='Your Information:\n\n'
	if C!=B:D+=f"**[UID]:** {C}\n\n"
	if isBanned(C):S=K.get('banReason','Unknown Reason');D+=f"**[🚫]Users is Currently Banned** Reason: {S}\n\n"
	L=getEventMessage()
	if L:D+=L+'\n\n'
	for(H,T)in G.items():
		if H!=Q and H not in items_data:D+=f"{H}: {T}\n"
	for(U,M)in items_data.items():
		V=M[Q];W=M['logo'];N=G.get(U,0)
		if N>0:D+=f"{W} {V}: {N}\n"
	if D.strip():await A.message.reply_text(D.strip(),parse_mode=O)
	else:await A.message.reply_text(getTextMap('errorRequest'))
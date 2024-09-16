from telegram import Update
from telegram.ext import CallbackContext
from handler.register import loadUserStatus,saveUserStatus,getTextMap
async def mods_command(update,context):
	L='mods';K='\n\n';J='isModerator';F='hidden';E=False;B=update;C=B.message.from_user.id;A=loadUserStatus();I=context.args
	if str(C)in A and A[str(C)].get(J,E):
		if len(I)>0 and I[0].lower()=='hide':
			M=A[str(C)].get(F,E);A[str(C)][F]=not M;saveUserStatus(A)
			if A[str(C)][F]:await B.message.reply_text(getTextMap('modHide'))
			else:await B.message.reply_text(getTextMap('modShow'))
			return
	G=[]
	for(O,H)in A.items():
		if H.get(J,E)and not H.get(F,E):N='@'+H.get('username','Unknown');G.append(N)
	if not G:D='Moderator List: (All are hidden)';D+=K+getTextMap(L);await B.message.reply_text(D)
	else:D='Moderator List: '+', '.join(G);D+=K+getTextMap(L);await B.message.reply_text(D)
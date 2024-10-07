from telegram import Update
from telegram.ext import CallbackContext
from handler.register import loadUserStatus,saveUserStatus,getTextMap,loadOwner
async def setacc_command(update,context):
	R='banExpires';Q='isRadio';P='isBanned';O='isHidden';N='isModerator';L='registered';K=context;J='OFF';I='ON';H=False;G=update;S=loadOwner()
	if not S==G.message.from_user.id:await G.message.reply_text(getTextMap('onlyOwner1'));return
	if len(K.args)<2:await G.message.reply_text(getTextMap('setUsage'));return
	E=K.args[0];D=K.args[1].lower();B=loadUserStatus();C=None
	for(M,T)in B.items():
		if str(M)==E or T.get('username','').lower()==E.lower():C=M;break
	if C is None:await G.message.reply_text(getTextMap('notFound'));return
	if D=='moderator'or D=='mod':A=B[C].get(N,H);B[C][N]=not A;F=f"Set Moderator for {E} to {I if not A else J}."
	elif D=='hide'or D=='hidden':A=B[C].get(O,H);B[C][O]=not A;F=f"Set Hidden for {E} to {I if not A else J}."
	elif D=='ban':A=B[C].get(P,H);B[C][P]=not A;F=f"Set Banned for {E} to {I if not A else J}."
	elif D=='register'or D=='regist'or D==L or D=='reg':A=B[C].get(L,H);B[C][L]=not A;F=f"Set Registered for {E} to {I if not A else J}."
	elif D=='radio':A=B[C].get(Q,H);B[C][Q]=not A;F=f"Set Radio for {E} to {I if not A else J}."
	elif D=='resetban'or D=='unban':
		A=B[C].get(R,0)
		if A==0:F=f"{E} is not banned.";return
		B[C][R]=0;F=f"Reset Ban for {E}."
	else:await G.message.reply_text(getTextMap('statsValue'));return
	saveUserStatus(B);await G.message.reply_text(F)
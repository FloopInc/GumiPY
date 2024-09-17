from telegram import Update
from telegram.ext import CallbackContext
from handler.register import loadUserStatus,saveUserStatus,getTextMap,loadConfig,isRegistered,isBanned
async def setacc_command(update,context):
	P='isRadio';O='isHidden';N='isModerator';L='registered';K=context;J='OFF';I='ON';H=False;B=update;Q=loadConfig()
	if not Q==B.message.from_user.id:await B.message.reply_text(getTextMap('onlyOwner1'));return
	if isBanned(B.message.from_user.id):await B.message.reply_text(getTextMap('isBanned'));return
	if not isRegistered(B.message.from_user.id):await B.message.reply_text(getTextMap('notRegistered'));return
	if len(K.args)<2:await B.message.reply_text(getTextMap('editUsage'));return
	F=K.args[0];E=K.args[1].lower();C=loadUserStatus();D=None
	for(M,R)in C.items():
		if str(M)==F or R.get('username','').lower()==F.lower():D=M;break
	if D is None:await B.message.reply_text(getTextMap('notFound'));return
	if E=='moderator'or E=='mod':A=C[D].get(N,H);C[D][N]=not A;G=f"Set Moderator for {F} to {I if not A else J}."
	elif E=='hide'or E=='hidden':A=C[D].get(O,H);C[D][O]=not A;G=f"Set Hidden for {F} to {I if not A else J}."
	elif E=='register'or E=='regist'or E==L or E=='reg':A=C[D].get(L,H);C[D][L]=not A;G=f"Set Registered for {F} to {I if not A else J}."
	elif E=='radio':A=C[D].get(P,H);C[D][P]=not A;G=f"Set Radio for {F} to {I if not A else J}."
	else:await B.message.reply_text(getTextMap('statsValue'));return
	saveUserStatus(C);await B.message.reply_text(G)
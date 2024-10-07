from telegram import Update
from telegram.ext import CallbackContext
from handler.register import getTextMap,loadOwner,isMod,loadUserProfile,saveUserProfile
from handler.profile import loadRedeemCode,saveRedeemCode,deleteRedeemCode
from handler.economy import loadItems
async def redeemcode_command(update,context):
	I='blacklist';H='count';B=update;F=B.message.from_user.id;J=loadUserProfile(F);K=loadItems();O=loadOwner();D=context.args
	if len(D)==0:await B.message.reply_text(getTextMap('redeemUsage'));return
	if F==O or isMod(F):
		if D[0].lower()=='create'or D[0].lower()=='c':
			if len(D)<4:await B.message.reply_text(getTextMap('redeemCreateUsage'));return
			E=D[1];P=int(D[2]);L={}
			for M in D[3:]:
				try:
					C,G=M.split(':');C=int(C);G=int(G)
					if str(C)not in K:await B.message.reply_text(f"Invalid item ID: {C}");return
					L[f"itemId{len(L)+1}"]={str(C):G}
				except ValueError:await B.message.reply_text(f"Invalid format for item: {M}");return
			A={H:P,**L,I:[]};saveRedeemCode(E,A);await B.message.reply_text(f"Redeem code '{E}' created successfully!");return
	E=D[0];A=loadRedeemCode(E)
	if not A:await B.message.reply_text('Invalid redeem code.');return
	if A[H]<=0:deleteRedeemCode(E);await B.message.reply_text('This redeem code is no longer available.');return
	if I in A and F in A[I]:await B.message.reply_text('You have already redeemed this code.');return
	N='Successfully redeemed:\n'
	for(Q,R)in A.items():
		if Q.startswith('itemId'):
			for(C,G)in R.items():J.setdefault(C,0);J[C]+=G;S=K[str(C)]['name'];T=K[str(C)]['logo'];N+=f"{T} {S}: {G}\n"
	A[H]-=1
	if A[H]<=0:deleteRedeemCode(E)
	A.setdefault(I,[]).append(F);saveUserProfile(F,J);saveRedeemCode(E,A);await B.message.reply_text(N)
import json,time
from handler.economy import loadItems
from handler.register import isBanned,isRegistered,loadUserProfile,saveUserProfile,getTextMap
def loadReward():
	with open('data/DailyReward.json','r')as A:B=json.load(A)
	return B
async def dailylogin_command(update,context):
	a='Error: Item not found.';Z='Markdown';V='logo';U='name';T='quantity';S='item_id';R='lastClaimTime';O='dailyLogin';C=update;F=C.message.from_user.id;b=C.message.text.strip();W=b.split(' ',1)
	if isBanned(F):await C.message.reply_text(isBanned(F),parse_mode=Z);return
	if not isRegistered(F):await C.message.reply_text(getTextMap('notRegistered'));return
	A=loadUserProfile(F);K=A.get(O,0);X=A.get(R,0);M=int(time.time());H=loadReward();P=loadItems()
	if len(W)>1 and W[1].lower()=='claim':
		if M-X<86400:Y=86400-(M-X);c=Y//3600;d=Y%3600//60;await C.message.reply_text(f"⏳ You can claim your daily login rewards again in {c} hours and {d} minutes.");return
		if K>=len(H):
			A[O]=1;A[R]=M;saveUserProfile(F,A);L=A[O];E=H[str(L)];D=E[S];G=E[T];B=P.get(D)
			if B:I=B[U];J=B[V];A[D]=A.get(D,0)+G;saveUserProfile(F,A);await C.message.reply_text(f"Day 7 Reward Claimed. You received: {J} {I} x{G} 🎉")
			else:await C.message.reply_text(a)
		else:
			L=K+1;E=H[str(L)];D=E[S];G=E[T];B=P.get(D)
			if B:I=B[U];J=B[V];A[D]=A.get(D,0)+G;A[O]=L;A[R]=M;saveUserProfile(F,A);await C.message.reply_text(f"Day {L} reward claimed: {J} {I} x{G} 🎉")
			else:await C.message.reply_text(a)
		return
	N='🎁 Daily Login Rewards 🎁\n\n'
	for Q in range(1,len(H)+1):
		E=H[str(Q)];D=E[S];G=E[T];B=P.get(D)
		if B:I=B[U];J=B[V]
		else:I='Unknown Item';J=''
		e='[CLAIMED]'if Q<=K else'[AVAILABLE]';N+=f"Day {Q}: {J} {I} x{G} {e}\n"
	if K<len(H):N+=f"\nUse `/dailylogin claim` to claim your Day {K+1} reward."
	else:N+='\nUse `/dailylogin claim` to claim your Day 1 reward.'
	await C.message.reply_text(N,parse_mode=Z)
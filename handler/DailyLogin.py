import json,time
from telegram import Update
from telegram.ext import ContextTypes
from handler.economy import loadItems
from handler.event import loadEventData
from handler.register import isBanned,isRegistered,loadUserProfile,saveUserProfile,getTextMap
def loadReward():
	with open('data/DailyReward.json','r')as A:B=json.load(A)
	return B
async def dailylogin_command(update,context):
	b='Error: Item not found.';a='Markdown';Z=False;V='logo';U='name';T='quantity';S='item_id';R='lastClaimTime';O='dailyLogin';B=update;F=B.message.from_user.id;c=B.message.text.strip();W=c.split(' ',1);d=loadEventData();e=d.get('WeeklyLogin',Z)
	if isBanned(F):await B.message.reply_text(isBanned(F),parse_mode=a);return
	if not isRegistered(F):await B.message.reply_text(getTextMap('notRegistered'));return
	if e==Z:await B.message.reply_text('Daily Login Event Not Active');return
	A=loadUserProfile(F);K=A.get(O,0);X=A.get(R,0);M=int(time.time());H=loadReward();P=loadItems()
	if len(W)>1 and W[1].lower()=='claim':
		if M-X<86400:Y=86400-(M-X);f=Y//3600;g=Y%3600//60;await B.message.reply_text(f"⏳ You can claim your daily login rewards again in {f} hours and {g} minutes.");return
		if K>=len(H):
			A[O]=1;A[R]=M;saveUserProfile(F,A);L=A[O];E=H[str(L)];D=E[S];G=E[T];C=P.get(D)
			if C:I=C[U];J=C[V];A[D]=A.get(D,0)+G;saveUserProfile(F,A);await B.message.reply_text(f"Day 7 Reward Claimed. You received: {J} {I} x{G} 🎉")
			else:await B.message.reply_text(b)
		else:
			L=K+1;E=H[str(L)];D=E[S];G=E[T];C=P.get(D)
			if C:I=C[U];J=C[V];A[D]=A.get(D,0)+G;A[O]=L;A[R]=M;saveUserProfile(F,A);await B.message.reply_text(f"Day {L} reward claimed: {J} {I} x{G} 🎉")
			else:await B.message.reply_text(b)
		return
	N='🎁 Daily Login Rewards 🎁\n\n'
	for Q in range(1,len(H)+1):
		E=H[str(Q)];D=E[S];G=E[T];C=P.get(D)
		if C:I=C[U];J=C[V]
		else:I='Unknown Item';J=''
		h='[CLAIMED]'if Q<=K else'[AVAILABLE]';N+=f"Day {Q}: {J} {I} x{G} {h}\n"
	if K<len(H):N+=f"\nUse `/dailylogin claim` to claim your Day {K+1} reward."
	else:N+='\nUse `/dailylogin claim` to claim your Day 1 reward.'
	await B.message.reply_text(N,parse_mode=a)
_A=None
from telegram import Update
from telegram.ext import ContextTypes
from command import dailyquest
from handler.register import loadUserProfile,saveUserProfile,getTextMap
from handler.economy import loadItems
from handler.register import loadOwner
import os
ownerID=loadOwner()
def findUserByName(target_name):
	B='.json';D='user/'
	for A in os.listdir(D):
		if A.endswith(B):
			C=loadUserProfile(A.replace(B,''))
			if C.get('name','').lower()==target_name.lower():return C,A.replace(B,'')
	return _A,_A
async def editacc_command(update,context):
	L='logs';J='valueMustBeNumber';C=update;I=C.message.from_user.id;G=context.args
	if I!=ownerID:await C.message.reply_text(getTextMap('onlyOwner'));return
	if len(G)<3:await C.message.reply_text(getTextMap('editUsage'));return
	E=G[0];B=G[1].lower();A=G[2];D,I=findUserByName(E)
	if not D:await C.message.reply_text(getTextMap('notFound'));return
	K=loadItems()
	if B=='dqid'or B=='dq':
		M=dailyquest.load_quests()
		if A not in M:await C.message.reply_text(getTextMap('invalidQuestId'));return
		D['dailyQuestId']=A;F=f"Updated daily quest ID for {E} to {A}."
	elif B=='dqclaim'or B=='dqc':
		if not A.isdigit():await C.message.reply_text(getTextMap(J));return
		D['dailyQuestLastClaim']=int(A);F=f"Updated daily quest last claim time for {E} to {A}."
	elif B=='dailylogin'or B=='dl':
		if not A.isdigit()or int(A)<1 or int(A)>7:await C.message.reply_text('Day must be a number between 1 and 7.');return
		D['dailyLogin']=int(A);F=f"Updated daily login for {E} to {A}."
	elif B=='dailyclaim'or B=='dlc':
		if not A.isdigit():await C.message.reply_text(getTextMap(J));return
		D['lastClaimTime']=int(A);F=f"Updated daily login last claim time for {E} to {A}."
	elif B=='clearlogs'or B==L:D[L]=[];F=f"Cleared logs for {E}."
	else:
		H=_A
		for(N,O)in K.items():
			if O['name'].lower()==B:H=N;break
		if H is _A:await C.message.reply_text(f"Item '{B}' not found in items.");return
		try:D[H]=int(A);F=f"Updated {B} ({K[H]['logo']}) for {E} to {A}."
		except ValueError:await C.message.reply_text(getTextMap(J));return
	saveUserProfile(I,D);await C.message.reply_text(F)
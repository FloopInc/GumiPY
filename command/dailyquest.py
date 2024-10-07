import json,random,time
from telegram import Update
from telegram.ext import ContextTypes
from handler.economy import loadItems
from handler.register import loadUserProfile,saveUserProfile,isBanned,isRegistered,getTextMap
def load_quests():
	with open('data/DailyQuest.json','r')as A:return json.load(A)
async def dailyquest_command(update,context):
	b='give';a='questions';U='reward';T='logo';S='Questions';R='dailyQuestLastClaim';N=context;M='description';L='type';J='dailyQuestId';H='name';G='Markdown';C=update;O=load_quests();I=loadItems();D=C.message.from_user.id;B=loadUserProfile(D)
	if isBanned(D):await C.message.reply_text(isBanned(D),parse_mode=G);return
	if not isRegistered(D):await C.message.reply_text(getTextMap('notRegistered'));return
	if J in B:
		V=B.get(R,0);W=int(time.time())
		if W-V<86400:X=86400-(W-V);c=X//3600;d=X%3600//60;await C.message.reply_text(f"⏳ You have already claimed your quest! Please wait {c} hours and {d} minutes before claiming again.");return
		A=O[B[J]]
		if not N.args:
			if A[L]==S:await C.message.reply_text(f"""📚 >Today's Quest: {A[H]}!< 🌟
{A[M]}

*Question:* ❓ _{A[a]}_

💬 To complete this quest, answer the question using `/dailyquest <your answer>`""",parse_mode=G)
			else:await C.message.reply_text(f"🚀 *Today's Quest: {A[H]}!* 🌟\n{A[M]}\n\n🎁 To complete this quest, you must do `/dailyquest give`.",parse_mode=G)
			return
		e=N.args[0].lower()
		if A[L]=='Deliver'and e==b:
			Y=A[b];f=all(B.get(C,0)>=D for A in Y for(C,D)in A.items())
			if f:
				g=[]
				for h in Y:
					for(P,E)in h.items():B[P]-=E;g.append(f"{I[P][T]} {I[P][H]} x{E}")
				K=[]
				for Q in A[U]:
					for(F,E)in Q.items():B[F]=B.get(F,0)+E;K.append(f"{I[F][T]} {I[F][H]} x{E}")
				saveUserProfile(D,B);await C.message.reply_text(f"🎉 *Congratulations!* You have completed the quest and received:\n"+'\n'.join(K),parse_mode=G);B[R]=int(time.time());B.pop(J,None);saveUserProfile(D,B)
			else:await C.message.reply_text("🚫 You don't have the required items to complete this quest!")
		elif A[L]==S:
			i=A['answers'].lower().strip();j=' '.join(N.args).lower().strip()
			if j==i:
				B[R]=int(time.time())
				for Q in A[U]:
					for(F,E)in Q.items():B[F]=B.get(F,0)+E
				saveUserProfile(D,B);K=[f"{I[A][T]} {I[A][H]} x{C}"for B in A[U]for(A,C)in B.items()];await C.message.reply_text(f"🎉 *Correct answer!* You received the following rewards:\n"+'\n'.join(K),parse_mode=G);B.pop(J,None);saveUserProfile(D,B)
			else:await C.message.reply_text("❌ That's not the correct answer! Please try again.")
	else:
		Z=random.choice(list(O.keys()));A=O[Z];B[J]=Z;saveUserProfile(D,B)
		if A[L]==S:await C.message.reply_text(f"""📚 *Today's Quest: {A[H]}!* 🌟
{A[M]}

*Question:* ❓ _{A[a]}_

💬 To complete this quest, answer the question using `/dailyquest <your answer>`""",parse_mode=G)
		else:await C.message.reply_text(f"🚀 *Today's Quest: {A[H]}!* 🌟\n{A[M]}\n\n🎁 To complete this quest, you must do `/dailyquest give`.",parse_mode=G)
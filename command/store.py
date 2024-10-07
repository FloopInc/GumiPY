from telegram import Update
from telegram.ext import CallbackContext
from handler.event import getEventMessage
from handler.store import getStoreItems,buyItem,sellItem
from handler.register import isRegistered,isBanned,getTextMap
async def store_command(update,context):
	N='sell';M='message';L='buy';G=' ';B=update;I=getStoreItems();A=context.args
	if isBanned(B.message.from_user.id):await B.message.reply_text(isBanned(B.message.from_user.id),parse_mode='Markdown');return
	if not isRegistered(B.message.from_user.id):await B.message.reply_text(getTextMap('notRegistered'));return
	if A:
		J=A[0].lower()
		if J==L:
			if len(A)>=2:
				if A[-1].isdigit():D=G.join(A[1:-1]);E=int(A[-1])
				else:D=G.join(A[1:]);E=1
				H=buyItem(B.message.from_user.id,D,E);await B.message.reply_text(H[M])
			return
		elif J==N:
			if len(A)>=2:
				if A[-1].isdigit():D=G.join(A[1:-1]);E=int(A[-1])
				else:D=G.join(A[1:]);E=1
				H=sellItem(B.message.from_user.id,D,E);await B.message.reply_text(H[M])
			return
	if not I:await B.message.reply_text('No items available in the store.');return
	C='🛒 Welcome to the Store! Here are the available items:\n\n';K=getEventMessage()
	if K:C+=K+'\n\n'
	for F in I:C+=f"{F['logo']} {F['name']}\n";C+=f"Price: {F[L]} 💵 Money\n";C+=f"Sell: {F[N]} 💵 Money\n";C+=f"{F['stock_message']}\n\n"
	await B.message.reply_text(C)
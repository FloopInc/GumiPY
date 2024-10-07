_G='Recipient not found.'
_F='data/items.json'
_E='user/'
_D='name'
_C='w'
_B='r'
_A='message'
import os,json,random,colorama,time
def loadItems():
	with open(_F,_B)as A:return json.load(A)
def saveItems(items):
	with open(_F,_C)as A:json.dump(items,A,indent=4)
def loadItemMapping():A=loadItems();return{B[_D]:A for(A,B)in A.items()}
def loadGachaConfig():
	with open('data/GachaConfig.json',_B)as A:return json.load(A)
def usercd(user_id,username):
	B=_E;C=os.path.join(B,f"{user_id}.json")
	if not os.path.exists(B):os.makedirs(B)
	E=loadItems();F={A:0 for A in E.keys()}
	if os.path.exists(C):
		with open(C,_B)as D:A=json.load(D)
	else:A={}
	A.setdefault(_D,username);A.setdefault('dailyLogin',0);A.setdefault('lastClaimTime',0);A.setdefault('logs',[]);A.setdefault('banReason','');A.setdefault('1000',5000)
	for(G,H)in F.items():A.setdefault(G,H)
	with open(C,_C)as D:json.dump(A,D,indent=4)
def performGacha(user_id,boxIdorName=None):
	P='logo';O='quantity';K=boxIdorName;I='item_id';H='1008';G='1007';S=loadItems();L=loadGachaConfig();J={'Mystery Box':G,'Super Mystery Box':H};E=f"user/{user_id}.json"
	if not os.path.exists(E):return{_A:'User data not found.'}
	with open(E,_B)as D:B=json.load(D)
	if K:
		A=K
		if A in J.values():0
		elif A in J:A=J[A]
		else:return{_A:'Invalid box ID or name.'}
	elif G in B and B[G]>0:A=G
	elif H in B and B[H]>0:A=H
	else:return{_A:"You don't have any gacha items to perform."}
	if A not in B or B[A]<=0:return{_A:"You don't have this item to perform gacha."}
	B[A]-=1
	if B[A]<=0:B[A]=0
	with open(E,_C)as D:json.dump(B,D,indent=4)
	if A not in L:return{_A:'Invalid box ID.'}
	Q=L[A]
	if random.random()<.9:M='noob_item'
	else:M='rare_item'
	R=Q[M];C=random.choice(R);B.setdefault(C[I],0);B[C[I]]+=C[O]
	with open(E,_C)as D:json.dump(B,D,indent=4)
	F=loadItems();N=f"Congratulations! From Gacha {F[A][P]} {F[A][_D]} You've received the following reward:\n";N+=f"{F[C[I]][P]} {F[C[I]][_D]} x{C[O]}";return{_A:N}
def giveItem(from_user_id,toUserName,item_name,quantity):
	L=from_user_id;H=toUserName;E=item_name;D=quantity;M=loadItemMapping();B=M.get(E)
	if not B:return{_A:f"Item '{E}' not found."}
	F=_E;I=os.path.join(F,f"{L}.json")
	if not os.path.exists(I):return{_A:"Sender's data not found."}
	with open(I,_B)as A:C=json.load(A)
	if B not in C or C[B]<D:return{_A:'Insufficient quantity to give.'}
	C[B]-=D
	if C[B]<=0:C[B]=0
	with open(I,_C)as A:json.dump(C,A,indent=4)
	G=None
	for J in os.listdir(F):
		if J.endswith('.json'):
			with open(os.path.join(F,J),_B)as A:
				N=json.load(A)
				if N.get(_D)==H:G=os.path.join(F,J);break
	if not G:return{_A:_G}
	with open(G,_B)as A:K=json.load(A)
	K.setdefault(B,0);K[B]+=D
	with open(G,_C)as A:json.dump(K,A,indent=4)
	print(f"[{int(time.time())%86400//3600:02d}:{int(time.time())%3600//60:02d}:{time.time()%60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] {L}/{C[_D]} gave {D} of item {E} to {H}.");return{_A:f"Successfully gave {D} of item {E} to {H}."}
def modGiveItem(from_user_id,toUserName,item_name,quantity):
	F=quantity;E=item_name;D=toUserName;J=loadItemMapping();B=J.get(E)
	if not B:return{_A:f"Item '{B}' not found."}
	G=_E;C=None
	for H in os.listdir(G):
		if H.endswith('.json'):
			with open(os.path.join(G,H),_B)as A:
				K=json.load(A)
				if K.get(_D)==D:C=os.path.join(G,H);break
	if not C:return{_A:_G}
	with open(C,_B)as A:I=json.load(A)
	I.setdefault(B,0);I[B]+=F
	with open(C,_C)as A:json.dump(I,A,indent=4)
	print(f"[{int(time.time())%86400//3600:02d}:{int(time.time())%3600//60:02d}:{time.time()%60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] {from_user_id} gave {F} of item {E} to {D}.");return{_A:f"During proccessing the command, i found out you're the bot owner. Now You won't lose any items from your inventory.\n\nSuccessfully gave {F} of item {E} to {D} without affecting your inventory."}
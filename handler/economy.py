_M='Recipient not found.'
_L='data/items.json'
_K='user/'
_J='rare_item'
_I='noob_item'
_H='1008'
_G='1007'
_F='name'
_E='w'
_D='r'
_C='quantity'
_B='message'
_A='item_id'
import os,json,random
def loadItems():
	with open(_L,_D)as A:return json.load(A)
def saveItems(items):
	with open(_L,_E)as A:json.dump(items,A,indent=4)
def loadItemMapping():A=loadItems();return{B[_F]:A for(A,B)in A.items()}
def loadGachaConfig():C='1005';B='1002';A='1001';return{_G:{_I:[{_A:A,_C:1},{_A:B,_C:1}],_J:[{_A:C,_C:1},{_A:_H,_C:1}]},_H:{_I:[{_A:A,_C:1},{_A:B,_C:1},{_A:C,_C:1}],_J:[{_A:A,_C:5},{_A:B,_C:3},{_A:'1003',_C:1},{_A:_G,_C:1}]}}
def usercd(user_id,username):
	B=_K;C=os.path.join(B,f"{user_id}.json")
	if not os.path.exists(B):os.makedirs(B)
	E=loadItems();F={A:0 for A in E.keys()}
	if os.path.exists(C):
		with open(C,_D)as D:A=json.load(D)
	else:A={}
	A.setdefault(_F,username)
	for(G,H)in F.items():A.setdefault(G,H)
	with open(C,_E)as D:json.dump(A,D,indent=4)
def performGacha(user_id,boxIdorName=None):
	L='logo';H=boxIdorName;O=loadItems();I=loadGachaConfig();G={'Mystery Box':_G,'Super Mystery Box':_H};E=f"user/{user_id}.json"
	if not os.path.exists(E):return{_B:'User data not found.'}
	with open(E,_D)as D:B=json.load(D)
	if H:
		A=H
		if A in G.values():0
		elif A in G:A=G[A]
		else:return{_B:'Invalid box ID or name.'}
	elif _G in B and B[_G]>0:A=_G
	elif _H in B and B[_H]>0:A=_H
	else:return{_B:"You don't have any gacha items to perform."}
	if A not in B or B[A]<=0:return{_B:"You don't have this item to perform gacha."}
	B[A]-=1
	if B[A]<=0:B[A]=0
	with open(E,_E)as D:json.dump(B,D,indent=4)
	if A not in I:return{_B:'Invalid box ID.'}
	M=I[A]
	if random.random()<.9:J=_I
	else:J=_J
	N=M[J];C=random.choice(N);B.setdefault(C[_A],0);B[C[_A]]+=C[_C]
	with open(E,_E)as D:json.dump(B,D,indent=4)
	F=loadItems();K=f"Congratulations! From Gacha {F[A][L]} {F[A][_F]} You've received the following reward:\n";K+=f"{F[C[_A]][L]} {F[C[_A]][_F]} x{C[_C]}";return{_B:K}
def giveItem(from_user_id,toUserName,item_name,quantity):
	K=toUserName;G=item_name;D=quantity;L=loadItemMapping();B=L.get(G)
	if not B:return{_B:f"Item '{G}' not found."}
	E=_K;H=os.path.join(E,f"{from_user_id}.json")
	if not os.path.exists(H):return{_B:"Sender's data not found."}
	with open(H,_D)as A:C=json.load(A)
	if B not in C or C[B]<D:return{_B:'Insufficient quantity to give.'}
	C[B]-=D
	if C[B]<=0:C[B]=0
	with open(H,_E)as A:json.dump(C,A,indent=4)
	F=None
	for I in os.listdir(E):
		if I.endswith('.json'):
			with open(os.path.join(E,I),_D)as A:
				M=json.load(A)
				if M.get(_F)==K:F=os.path.join(E,I);break
	if not F:return{_B:_M}
	with open(F,_D)as A:J=json.load(A)
	J.setdefault(B,0);J[B]+=D
	with open(F,_E)as A:json.dump(J,A,indent=4)
	return{_B:f"Successfully gave {D} of item {G} to {K}."}
def modGiveItem(from_user_id,toUserName,item_name,quantity):
	I=quantity;H=item_name;G=toUserName;J=loadItemMapping();B=J.get(H)
	if not B:return{_B:f"Item '{B}' not found."}
	D=_K;C=None
	for E in os.listdir(D):
		if E.endswith('.json'):
			with open(os.path.join(D,E),_D)as A:
				K=json.load(A)
				if K.get(_F)==G:C=os.path.join(D,E);break
	if not C:return{_B:_M}
	with open(C,_D)as A:F=json.load(A)
	F.setdefault(B,0);F[B]+=I
	with open(C,_E)as A:json.dump(F,A,indent=4)
	return{_B:f"During proccessing the command, i found out you're the bot owner. Now You won't lose any items from your inventory.\n\nSuccessfully gave {I} of item {H} to {G} without affecting your inventory."}
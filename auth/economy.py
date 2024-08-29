_G='rare_item'
_F='noob_item'
_E='name'
_D='1008'
_C='1007'
_B='quantity'
_A='item_id'
import os,json,random
def loadItems():
	with open('data/items.json','r')as A:return json.load(A)
def loadItemMapping():A=loadItems();return{B[_E]:A for(A,B)in A.items()}
def loadGachaConfig():F='1006';E='1005';D='1004';C='1003';B='1002';A='1001';return{_C:{_F:[{_A:A,_B:1},{_A:B,_B:1},{_A:C,_B:3},{_A:D,_B:3}],_G:[{_A:E,_B:1},{_A:F,_B:1},{_A:_C,_B:1},{_A:_D,_B:1}]},_D:{_F:[{_A:A,_B:2},{_A:B,_B:2},{_A:C,_B:5},{_A:D,_B:5}],_G:[{_A:E,_B:2},{_A:F,_B:2},{_A:_C,_B:2},{_A:_D,_B:2}]}}
def usercd(user_id,username):
	B='user/';C=os.path.join(B,f"{user_id}.json")
	if not os.path.exists(B):os.makedirs(B)
	E=loadItems();F={A:0 for A in E.keys()}
	if os.path.exists(C):
		with open(C,'r')as D:A=json.load(D)
	else:A={}
	A.setdefault('money',0);A.setdefault(_E,username)
	for(G,H)in F.items():A.setdefault(G,H)
	with open(C,'w')as D:json.dump(A,D,indent=4)
def performGacha(user_id,boxIdorName=None):
	M='logo';I=boxIdorName;D='message';P=loadItems();J=loadGachaConfig();H={'Mystery Box':_C,'Super Mystery Box':_D};F=f"user/{user_id}.json"
	if not os.path.exists(F):return{D:'User data not found.'}
	with open(F,'r')as E:B=json.load(E)
	if I:
		A=I
		if A in H.values():0
		elif A in H:A=H[A]
		else:return{D:'Invalid box ID or name.'}
	elif _C in B and B[_C]>0:A=_C
	elif _D in B and B[_D]>0:A=_D
	else:return{D:"You don't have any gacha items to perform."}
	if A not in B or B[A]<=0:return{D:"You don't have this item to perform gacha."}
	B[A]-=1
	if B[A]<=0:B[A]=0
	with open(F,'w')as E:json.dump(B,E,indent=4)
	if A not in J:return{D:'Invalid box ID.'}
	N=J[A]
	if random.random()<.5:K=_F
	else:K=_G
	O=N[K];C=random.choice(O);B.setdefault(C[_A],0);B[C[_A]]+=C[_B]
	with open(F,'w')as E:json.dump(B,E,indent=4)
	G=loadItems();L=f"Congratulations! From Gacha {G[A][M]} {G[A][_E]} You've received the following reward:\n";L+=f"{G[C[_A]][M]} {G[C[_A]][_E]} x{C[_B]}";return{D:L}
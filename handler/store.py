_M='data/items.json'
_L='User data not found.'
_K='Out of order!'
_J='Currently unavailable!'
_I='Out of stock!'
_H='1000'
_G='sell'
_F='buy'
_E='logo'
_D='untradeable'
_C='stock'
_B='name'
_A='message'
import os,json,random,time,colorama
from handler.economy import loadItems
from handler.register import getTextMap
def getStoreItems():
	D=loadItems();B=[]
	for(E,A)in D.items():
		if A.get(_D):continue
		if A[_C]==0:F=[_I,_J,_K,'Check back later!'];C=random.choice(F)
		else:C=f"Stock: {A[_C]}"
		B.append({'id':E,_B:A[_B],_E:A[_E],_F:A[_F],_G:A[_G],'stock_message':C})
	return B
def buyItem(user_id,item_name,quantity):
	J=item_name;I=user_id;D=quantity;B=loadItems();H=f"user/{I}.json"
	if not os.path.exists(H):return{_A:_L}
	with open(H,'r')as E:F=json.load(E)
	A=None
	for(K,L)in B.items():
		if L[_B].lower()==J.lower():A=K;break
	if not A or A not in B:return{_A:f"Item '{J}' not found in store."}
	C=B[A]
	if C.get(_D):return{_A:getTextMap(_D)}
	if C[_C]==0:return{_A:random.choice([_I,_J,_K])}
	G=C[_F]*D
	if F[_H]<G:return{_A:getTextMap('notEnoughMoney')}
	F[_H]-=G;B[A][_C]-=D
	if B[A][_C]<0:B[A][_C]=0
	F.setdefault(A,0);F[A]+=D
	with open(H,'w')as E:json.dump(F,E,indent=4)
	with open(_M,'w')as E:json.dump(B,E,indent=4)
	print(f"[{int(time.time())%86400//3600:02d}:{int(time.time())%3600//60:02d}:{time.time()%60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] User {I} bought {D} x {C[_B]} for {G} 💵 Money!");return{_A:f"Successfully purchased {D} x {C[_E]} {C[_B]} for {G} 💵 Money!"}
def sellItem(user_id,item_name,quantity):
	J=item_name;I=user_id;B=quantity;D=loadItems();G=f"user/{I}.json"
	if not os.path.exists(G):return{_A:_L}
	with open(G,'r')as E:C=json.load(E)
	A=None
	for(K,L)in D.items():
		if L[_B].lower()==J.lower():A=K;break
	if not A or A not in D:return{_A:f"Item '{J}' not found in inventory."}
	F=D[A]
	if F.get(_D):return{_A:getTextMap(_D)}
	if C.get(A,0)<B:return{_A:"You don't have that item to sell"}
	H=F[_G]*B;C[A]-=B
	if C[A]<0:C[A]=0
	C[_H]+=H;D[A][_C]+=B
	with open(G,'w')as E:json.dump(C,E,indent=4)
	with open(_M,'w')as E:json.dump(D,E,indent=4)
	print(f"[{int(time.time())%86400//3600:02d}:{int(time.time())%3600//60:02d}:{time.time()%60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] User {I} sold {B} x {F[_B]} for {H} 💵 Money!");return{_A:f"Successfully sold {B} x {F[_E]} {F[_B]} for {H} 💵 Money!"}
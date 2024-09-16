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
_C='name'
_B='stock'
_A='message'
import os,json,random
from handler.economy import loadItems
from handler.register import getTextMap
def getStoreItems():
	D=loadItems();B=[]
	for(E,A)in D.items():
		if A.get(_D):continue
		if A[_B]==0:F=[_I,_J,_K,'Check back later!'];C=random.choice(F)
		else:C=f"Stock: {A[_B]}"
		B.append({'id':E,_C:A[_C],_E:A[_E],_F:A[_F],_G:A[_G],'stock_message':C})
	return B
def buyItem(user_id,item_name,quantity):
	I=item_name;F=quantity;B=loadItems();G=f"user/{user_id}.json"
	if not os.path.exists(G):return{_A:_L}
	with open(G,'r')as C:D=json.load(C)
	A=None
	for(J,K)in B.items():
		if K[_C].lower()==I.lower():A=J;break
	if not A or A not in B:return{_A:f"Item '{I}' not found in store."}
	E=B[A]
	if E.get(_D):return{_A:getTextMap(_D)}
	if E[_B]==0:return{_A:random.choice([_I,_J,_K])}
	H=E[_F]*F
	if D[_H]<H:return{_A:getTextMap('notEnoughMoney')}
	D[_H]-=H;B[A][_B]-=F
	if B[A][_B]<0:B[A][_B]=0
	D.setdefault(A,0);D[A]+=F
	with open(G,'w')as C:json.dump(D,C,indent=4)
	with open(_M,'w')as C:json.dump(B,C,indent=4)
	return{_A:f"Successfully purchased {F} x {E[_E]} {E[_C]} for {H} 💵 Money!"}
def sellItem(user_id,item_name,quantity):
	H=item_name;C=quantity;D=loadItems();G=f"user/{user_id}.json"
	if not os.path.exists(G):return{_A:_L}
	with open(G,'r')as E:B=json.load(E)
	A=None
	for(J,K)in D.items():
		if K[_C].lower()==H.lower():A=J;break
	if not A or A not in D:return{_A:f"Item '{H}' not found in inventory."}
	F=D[A]
	if F.get(_D):return{_A:getTextMap(_D)}
	if B.get(A,0)<C:return{_A:"You don't have that item to sell"}
	I=F[_G]*C;B[A]-=C
	if B[A]<0:B[A]=0
	B[_H]+=I;D[A][_B]+=C
	with open(G,'w')as E:json.dump(B,E,indent=4)
	with open(_M,'w')as E:json.dump(D,E,indent=4)
	return{_A:f"Successfully sold {C} x {F[_E]} {F[_C]} for {I} 💵 Money!"}
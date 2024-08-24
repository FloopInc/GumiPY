import os,json
def usercd(user_id,username):
	B='user/auth';C=os.path.join(B,f"{user_id}.json")
	if not os.path.exists(B):os.makedirs(B)
	if os.path.exists(C):
		with open(C,'r')as D:A=json.load(D)
	else:A={}
	A.setdefault('money',0);A.setdefault('name',username)
	with open(C,'w')as D:json.dump(A,D)
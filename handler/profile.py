import json,os
from handler.register import loadUserStatus,loadConfig
STATUSFILE='data/UserStatus.json'
def loadUserProfile(user_id):
	A=f"user/{user_id}.json"
	if os.path.exists(A):
		with open(A,'r')as B:return json.load(B)
	return{}
def saveUserProfile(user_id,profile_data):
	A=f"user/{user_id}.json"
	with open(A,'w')as B:json.dump(profile_data,B,indent=4)
def getUserIdFromUsername(username):
	A=loadUserStatus()
	for(B,C)in A.items():
		if C.get('username','').lower()==username.lower():return B
def inspectProfile(user_id):
	O='1010';N='1008';M='1007';L='1005';K='1003';J='1002';I='1001';H='1000';D='name';B=user_id;E=loadUserStatus();A=loadUserProfile(B);P=loadConfig();C={};F={'registered':'Account Registered','isBanned':'Account Banned'}
	if B==P:C={B:A[B]for B in[D,H,I,J,K,L,M,N,O]if B in A}
	elif str(B)in E:
		for(G,Q)in E[str(B)].items():
			if G in F:C[F[G]]='Yes'if Q else'No'
		C.update({B:A[B]for B in[D,H,I,J,K,L,M,N,O]if B in A})
	return C,A.get(D,'user')
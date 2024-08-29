import json,os
from handler.register import loadUserStatus,loadConfig
STATUSFILE='data/UserStatus.json'
def loadUserProfile(user_id):
	A=f"user/{user_id}.json"
	if os.path.exists(A):
		with open(A,'r')as B:return json.load(B)
	return{}
def inspectProfile(user_id):
	N='1008';M='1007';L='1005';K='1003';J='1002';I='1001';H='money';D='name';B=user_id;E=loadUserStatus();A=loadUserProfile(B);O=loadConfig();C={};F={'registered':'Account Registered','isBanned':'Account Banned'}
	if B==O:C={B:A[B]for B in[H,D,I,J,K,L,M,N]if B in A}
	elif str(B)in E:
		for(G,P)in E[str(B)].items():
			if G in F:C[F[G]]='Yes'if P else'No'
		C.update({B:A[B]for B in[H,D,I,J,K,L,M,N]if B in A})
	return C,A.get(D,'User')
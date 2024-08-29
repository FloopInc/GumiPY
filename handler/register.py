_E='notFound'
_D='isBanned'
_C=False
_B='registered'
_A='message'
import json,os
STATUSFILE='data/UserStatus.json'
PASSWORD='OZMoon'
TEXTMAP='data/TextMap.json'
def loadConfig():
	with open('data/config.json')as A:B=json.load(A);return B['Owner']
def loadUserStatus():
	if os.path.exists(STATUSFILE):
		with open(STATUSFILE,'r')as B:
			A=json.load(B)
			if isinstance(A,dict):return A
	return{}
def saveUserStatus(userStatus):
	with open(STATUSFILE,'w')as A:json.dump(userStatus,A,indent=4)
def loadTextMap():
	if os.path.exists(TEXTMAP):
		with open(TEXTMAP,'r')as A:return json.load(A)
	return{}
TextMap=loadTextMap()
def getTextMap(key):A=loadTextMap();return A.get(key,'')
def isRegistered(user_id):A=loadUserStatus();return A.get(str(user_id),{}).get(_B,_C)
def isBanned(user_id):A=loadUserStatus();return A.get(str(user_id),{}).get(_D,True)
def unregister(user_id):
	B=user_id;A=loadUserStatus()
	if str(B)in A:A[str(B)][_B]=_C;saveUserStatus(A);return{_A:getTextMap('unregisterSuccess')}
	return{_A:getTextMap(_E)}
def register(user_id,password):
	if password!=PASSWORD:return{_A:getTextMap('invalidPassword')}
	A=loadUserStatus()
	if not isinstance(A,dict):return{_A:getTextMap('internalError')}
	A[str(user_id)][_B]=True;saveUserStatus(A);return{_A:getTextMap('registerSuccess')}
def ban(user_id):
	B=user_id;A=loadUserStatus()
	if str(B)in A:A[str(B)][_D]=True;A[str(B)][_B]=_C;saveUserStatus(A);return{_A:getTextMap('banned')}
	return{_A:getTextMap(_E)}
def unban(user_id):
	B=user_id;A=loadUserStatus()
	if str(B)in A:A[str(B)][_D]=_C;saveUserStatus(A);return{_A:getTextMap('unbanned')}
	return{_A:getTextMap(_E)}
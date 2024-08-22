_E='User not found.'
_D='isBanned'
_C=False
_B='registered'
_A='message'
import json,os
STATUS_FILE='user/UserStatus.json'
REGISTER_PASSWORD='OZMoon'
def load_user_status():
	if os.path.exists(STATUS_FILE):
		with open(STATUS_FILE,'r')as B:
			A=json.load(B)
			if isinstance(A,dict):return A
	return{}
def save_user_status(user_status):
	with open(STATUS_FILE,'w')as A:json.dump(user_status,A,indent=4)
def is_registered(user_id):A=load_user_status();return A.get(str(user_id),{}).get(_B,_C)
def is_banned(user_id):A=load_user_status();return A.get(str(user_id),{}).get(_D,True)
def unregister(user_id):
	B=user_id;A=load_user_status()
	if str(B)in A:A[str(B)][_B]=_C;save_user_status(A);return{_A:'Unregistration successful. User can no longer use bot commands.'}
	return{_A:_E}
def register(user_id,password):
	if password!=REGISTER_PASSWORD:return{_A:'Invalid password'}
	A=load_user_status()
	if not isinstance(A,dict):return{_A:'Internal error: User status file is corrupted.'}
	A[str(user_id)][_B]=True;save_user_status(A);return{_A:'Registration successful. You can now use all bot commands.'}
def ban(user_id):
	B=user_id;A=load_user_status()
	if str(B)in A:A[str(B)][_D]=True;save_user_status(A);return{_A:'User has been banned.'}
	return{_A:_E}
def unban(user_id):
	B=user_id;A=load_user_status()
	if str(B)in A:A[str(B)][_D]=_C;save_user_status(A);return{_A:'User has been unbanned.'}
	return{_A:_E}
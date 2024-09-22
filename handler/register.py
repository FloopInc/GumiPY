_F='notFound'
_E='isBanned'
_D=True
_C=False
_B='registered'
_A='message'
import json,os
from telegram import Update
from telegram.ext import ContextTypes
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
def isMod(user_id):A=loadUserStatus();return A.get(str(user_id),{}).get('isModerator',_D)
def isBanned(user_id):A=loadUserStatus();return A.get(str(user_id),{}).get(_E,_D)
def unregister(user_id):
	B=user_id;A=loadUserStatus()
	if str(B)in A:A[str(B)][_B]=_C;saveUserStatus(A);return{_A:getTextMap('unregisterSuccess')}
	return{_A:getTextMap(_F)}
def register(user_id,password):
	if password!=PASSWORD:return{_A:getTextMap('invalidPassword')}
	A=loadUserStatus()
	if not isinstance(A,dict):return{_A:getTextMap('internalError')}
	A[str(user_id)][_B]=_D;saveUserStatus(A);return{_A:getTextMap('registerSuccess')}
def ban(user_id):
	B=user_id;A=loadUserStatus()
	if str(B)in A:A[str(B)][_E]=_D;A[str(B)][_B]=_C;saveUserStatus(A);return{_A:getTextMap('banned')}
	return{_A:getTextMap(_F)}
def unban(user_id):
	B=user_id;A=loadUserStatus()
	if str(B)in A:A[str(B)][_E]=_C;saveUserStatus(A);return{_A:getTextMap('unbanned')}
	return{_A:getTextMap(_F)}
async def register_command(update,context):
	A=update;B=A.message.from_user.id;C=A.message.text.strip();D=C.split(' ')[1]if len(C.split(' '))>1 else None
	if isBanned(B):await A.message.reply_text(getTextMap(_E));return
	if isRegistered(B):await A.message.reply_text(getTextMap(_B));return
	E=register(B,D);await A.message.reply_text(E[_E])
_M='reason'
_L='action'
_K='username'
_J='banReason'
_I='isModerator'
_H='notFound'
_G='banExpires'
_F=None
_E='isBanned'
_D='registered'
_C='logs'
_B=False
_A='message'
import json,os,random,time
from telegram import Update
from telegram.ext import ContextTypes
from colorama import Fore,Style
STATUSFILE='data/UserStatus.json'
PASSWORD='OZMoon'
TEXTMAP='data/TextMap.json'
def loadLargeJson():
	with open('data/TextMapEN.json','r')as A:return json.load(A)
def searchJson(keyword,data,limit=15):
	D=limit;A=[];B=set()
	for(F,E)in data.items():
		C=str(E)
		if keyword.lower()in C.lower()and C not in B:B.add(C);A.append(f"{E}")
	if len(A)>D:A=random.sample(A,D)
	return A,len(B)
def loadOwner():
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
def getTextMap(key):A=loadTextMap();return A.get(key,'')
def loadUserProfile(user_id):
	A=f"user/{user_id}.json"
	if os.path.exists(A):
		with open(A,'r')as B:return json.load(B)
	return{}
def saveUserProfile(user_id,profile_data):
	A=f"user/{user_id}.json"
	with open(A,'w')as B:json.dump(profile_data,B,indent=4)
def isRegistered(user_id):A=loadUserStatus();return A.get(str(user_id),{}).get(_D,_B)
def isMod(user_id):A=loadUserStatus();return A.get(str(user_id),{}).get(_I,True)
def format_remaining_time(seconds):A=seconds;B=A//(24*3600);A%=24*3600;C=A//3600;A%=3600;D=A//60;A%=60;return f"{B}d {C}h {D}m {A}s"
def isBanned(user_id):
	B=user_id;C=loadUserStatus();E=loadUserProfile(B);G=E.get(_J,'');J=E.get(_K,'');A=C.get(str(B),{})
	if not A.get(_E,_B):return
	D=A.get(_G,_F)
	if D is _F:return getTextMap(_E)
	F=int(time.time())
	if F<D:H=D-F;I=format_remaining_time(H);return f"🚫 Sorry, but Your Account has been temporarily suspended.\nBan Reason: `{G}`\nThis temporary ban will be removed in **{I}**. If you didn't do anything wrong & believe this is a mistake please contact /mods"
	else:A[_E]=_B;C[str(B)]=A;saveUserStatus(C);return
def unregister(user_id):
	B=user_id;A=loadUserStatus()
	if str(B)in A:A[str(B)][_D]=_B;saveUserStatus(A);return{_A:getTextMap('unregisterSuccess')}
	return{_A:getTextMap(_H)}
def register(user_id,password):
	C=password;A=user_id;B=loadUserStatus();D=B.get(str(A),{}).get(_K,'')
	if C!=PASSWORD:print(f"[{int(time.time())%86400//3600:02d}:{int(time.time())%3600//60:02d}:{time.time()%60:02.0f}] [{Fore.RED}ERROR{Style.RESET_ALL}] User {A}/{D} Input Invalid Password during register account: {C}");return{_A:getTextMap('invalidPassword')}
	if not isinstance(B,dict):return{_A:getTextMap('internalError')}
	B[str(A)][_D]=True;saveUserStatus(B);print(f"[{int(time.time())%86400//3600:02d}:{int(time.time())%3600//60:02d}:{time.time()%60:02.0f}] [{Fore.BLUE}INFO{Style.RESET_ALL}] User {A}/{D} registered account.");return{_A:getTextMap('registerSuccess')}
def ban(user_id,reason='',duration=0):
	E=duration;D=reason;A=user_id;B=loadUserStatus()
	if str(A)in B:
		B[str(A)][_E]=True;B[str(A)][_D]=_B;B[str(A)]['isRadio']=_B;B[str(A)][_I]=_B
		if E>0:B[str(A)][_G]=int(time.time())+E
		else:B[str(A)][_G]=_F
		saveUserStatus(B);C=loadUserProfile(A)
		if _C not in C:C[_C]=[]
		if D:C[_J]=D;C[_C].append({_L:'ban',_M:D})
		saveUserProfile(A,C);return{_A:getTextMap('banned')}
	return{_A:getTextMap(_H)}
def unban(user_id,reason=''):
	D=reason;A=user_id;B=loadUserStatus()
	if str(A)in B:
		B[str(A)][_E]=_B;B[str(A)][_G]=_F;saveUserStatus(B);C=loadUserProfile(A)
		if _C not in C:C[_C]=[]
		if D:C[_C].append({_L:'unban',_M:D})
		saveUserProfile(A,C);return{_A:getTextMap('unbanned')}
	return{_A:getTextMap(_H)}
async def register_command(update,context):
	A=update;B=A.message.from_user.id;C=A.message.text.strip();D=C.split(' ')[1]if len(C.split(' '))>1 else _F
	if isBanned(B):await A.message.reply_text(isBanned(B),parse_mode='Markdown');return
	if isRegistered(B):await A.message.reply_text(getTextMap(_D));return
	E=register(B,D);await A.message.reply_text(E[_A])
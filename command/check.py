_B='msg'
_A='utf-8'
import requests,base64,json,re
from telegram import Update
from telegram.ext import ContextTypes
from handler.register import isRegistered,isBanned,getTextMap
with open('data/dispatch.json')as config_file:config_data=json.load(config_file)
async def check_version(update,context):
	A=update;D=context.args
	if isBanned(A.message.from_user.id):await A.message.reply_text(isBanned(A.message.from_user.id),parse_mode='Markdown');return
	if not isRegistered(A.message.from_user.id):await A.message.reply_text(getTextMap('notRegistered'));return
	if len(D)<2:await A.message.reply_text(getTextMap('provideVersion'));return
	B=D[0].lower();H=D[1]
	if B in['osstarrailbeta','ossrbeta']:C=config_data['os_sr_beta']
	elif B in['cnstarrailbeta','cnsrbeta']:C=config_data['cn_sr_beta']
	elif B in['osstarrailprod','ossrprod']:C=config_data['os_sr_prod']
	elif B in['cnstarrailprod','cnsrprod']:C=config_data['cn_sr_prod']
	else:await A.message.reply_text(getTextMap('invalidCheck'));return
	L=base64.b64decode(C).decode(_A);M=f"{L}{H}&language_type=3&platform_type=1&channel_id=1&sub_channel_id=1&is_new_format=1"
	try:
		E=requests.get(M);E.raise_for_status();F=base64.b64decode(E.content);N=decode_protobuf_message(F).get(_B,'No Message Found');I=f"""Response Status Code: {E.status_code}

Raw Message Content for Version {H}: {F}

Result Message: {N}

""";J=extract_urls(str(F))
		if J:K='URLs:\n'+'\n'.join(J)
		else:K='URLs: No URLs found.'
		I+=K;await A.message.reply_text(I)
	except requests.exceptions.RequestException as G:await A.message.reply_text(f"Error making request: {G}")
	except Exception as G:await A.message.reply_text(f"Error: {G}")
def decode_protobuf_message(data):
	N='ignore';G='regionList';C=data;B={};A=0
	while A<len(C):
		H=C[A];D=H>>3;F=H&7;A+=1
		if F==0:
			I=0;J=0
			while True:
				K=C[A];I|=(K&127)<<J;A+=1
				if K<128:break
				J+=7
			if D==1:B['retcode']=I
		elif F==2:
			L=C[A];A+=1;O=C[A:A+L];A+=L;P=O.decode(_A,errors=N);E=re.sub('[^\\w\\s,.!?]','',P)
			if D==2 or _B not in B:B[_B]=E
			elif D==3:B['top_sever_region_name']=E
			elif D==5:B['stop_desc']=E
			else:B[f"field_{D}"]=E
		elif F==2:
			M=C[A];A+=1;Q=C[A:A+M];A+=M
			if G not in B:B[G]=[]
			B[G].append(Q.decode(_A,errors=N))
	return B
def extract_urls(text):A=re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\\\(\\\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',text);return A
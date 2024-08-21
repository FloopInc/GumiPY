_A='utf-8'
import requests,base64,json,re,logging
from typing import Final
from telegram import Update
from telegram.ext import Application,CommandHandler,ContextTypes,MessageHandler,filters
from auth.register import register,is_registered
with open('config.json')as config_file:config_data=json.load(config_file)
log_file_path='log/logs.json'
if not log_file_path:
	with open(log_file_path,'w')as log_file:log_file.write('[]')
async def check_version(update,context):
	A=update;N=A.message.from_user.id;F=A.message.text.strip();C=F.split(' ')[1]if len(F.split(' '))>1 else None
	if not is_registered(A.message.from_user.id):await A.message.reply_text('You are not registered. Please register using /register <password>.');return
	if not C:await A.message.reply_text('Please provide a version number.');return
	K=config_data['url'];L=base64.b64decode(K).decode(_A);G=f"{L}{C}&language_type=3&platform_type=1&channel_id=1&sub_channel_id=1&is_new_format=1";B=requests.get(G);O=B.content
	try:
		B=requests.get(G);B.raise_for_status();D=base64.b64decode(B.content);M=decode_protobuf_message(D).get('msg','No Message Found');H=f"""Response Status Code: {B.status_code}

Raw Message Content for Version {C}: {D}

Result Message: {M}

""";I=extract_urls(str(D))
		if I:J='URLs:\n'+'\n'.join(I)
		else:J='URLs: No URLs found.'
		H+=J;await A.message.reply_text(H)
	except requests.exceptions.RequestException as E:await A.message.reply_text(f"Error making request: {E}")
	except Exception as E:await A.message.reply_text(f"Error: {E}")
def decode_protobuf_message(data):
	H='regionList';C=data;B={};A=0
	while A<len(C):
		I=C[A];D=I>>3;E=I&7;A+=1
		if E==0:
			J=0;K=0;F=0
			while F&128:F=C[A];J|=(F&127)<<K;A+=1;K+=7
			if D==1:B['retcode']=J
		elif E==2:
			L=C[A];A+=1;G=C[A:A+L];A+=L
			if D==2:B['msg']=G.decode(_A)
			elif D==3:B['top_sever_region_name']=G.decode(_A)
			elif D==5:B['stop_desc']=G.decode(_A)
		elif E==2:
			M=C[A];A+=1;N=C[A:A+M];A+=M
			if H not in B:B[H]=[]
			B[H].append(N.decode(_A))
	return B
def extract_urls(text):A=re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\\\(\\\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',text);return A
import requests,base64,json,re,tempfile,blackboxprotobuf
from telegram import Update
from telegram.ext import ContextTypes
from handler.register import isRegistered,isBanned,getTextMap
with open('data/dispatch.json')as config_file:config_data=json.load(config_file)
async def hotfix_command(update,context):
	A0='preDownloadUrl';z='provideCurData';y='cnprodsr';x='prodsrcn';w='srprodcn';v='cnsrprod';u='moprodsr';t='hkprodsr';s='twprodsr';r='chtprodsr';q='prodsrcht';p='srprodcht';o='chtsrprod';n='eurprodsr';m='prodsreur';l='srprodeur';k='eursrprod';j='usaprodsr';i='prodsrusa';h='srprodusa';g='usasrprod';f='asiaprodsr';e='prodsrasia';d='srprodasia';c='asiasrprod';b='cnbetasr';a='betacnsr';Z='srbetacn';Y='cnsrbeta';X='usabetasr';W='betausasr';V='srbetausa';U='usasrbeta';T='asiabetasr';S='betaasiasr';R='srbetaasia';Q='asiasrbeta';M='ifixUrl';L='luaUrl';K='exResourceUrl';J='assetBundleUrl';C=update;F=context.args
	if isBanned(C.message.from_user.id):await C.message.reply_text(isBanned(C.message.from_user.id),parse_mode='Markdown');return
	if not isRegistered(C.message.from_user.id):await C.message.reply_text(getTextMap('notRegistered'));return
	if len(F)<3:await C.message.reply_text(getTextMap('invalidReq'));return
	A=F[0].lower();B=F[1];G=F[2]
	if A in[Q,R,S,T]:D=config_data['beta_release01_asia']or config_data['beta_release02_asia']
	elif A in[U,V,W,X]:D=config_data['beta_release01_usa']or config_data['beta_release02_usa']
	elif A in[Y,Z,a,b]:D=config_data['beta_release01_cn']or config_data['beta_release02_cn']or config_data['beta_release03_cn']
	elif A in[c,d,e,f]:D=config_data['prod_official_asia']
	elif A in[g,h,i,j]:D=config_data['prod_official_usa']
	elif A in[k,l,m,n]:D=config_data['prod_official_eur']
	elif A in[o,p,q,r,s,t,u]:D=config_data['prod_official_cht']
	elif A in[v,w,x,y]:D=config_data['prod_gf_cn']
	else:await C.message.reply_text(getTextMap(z));return
	A1={J:f"https://autopatchos.starrails.com/asb/V{B}Live/[\\w_-]+",K:f"https://autopatchos.starrails.com/design_data/V{B}Live/[\\w_-]+",L:f"https://autopatchos.starrails.com/lua/V{B}Live/[\\w_-]+",M:f"https://autopatchos.starrails.com/ifix/V{B}Live/[\\w_-]+",A0:f"https://autopatchos.starrails.com/pre_download/V2.7Live/[\\w_-]+"};A2={J:f"https://autopatchcn.bhsr.com/asb/V{B}Live/[\\w_-]+",K:f"https://autopatchcn.bhsr.com/design_data/V{B}Live/[\\w_-]+",L:f"https://autopatchcn.bhsr.com/lua/V{B}Live/[\\w_-]+",M:f"https://autopatchcn.bhsr.com/ifix/V{B}Live/[\\w_-]+",A0:f"https://autopatchcn.bhsr.com/pre_download/V2.7Live/[\\w_-]+"};A3={J:f"https://autopatchcn.bhsr.com/asb/BetaLive/[\\w_-]+",K:f"https://autopatchcn.bhsr.com/design_data/BetaLive/[\\w_-]+",L:f"https://autopatchcn.bhsr.com/lua/BetaLive/[\\w_-]+",M:f"https://autopatchcn.bhsr.com/ifix/BetaLive/[\\w_-]+"};A4={J:f"https://autopatchos.starrails.com/asb/BetaLive/[\\w_-]+",K:f"https://autopatchos.starrails.com/design_data/BetaLive/[\\w_-]+",L:f"https://autopatchos.starrails.com/lua/BetaLive/[\\w_-]+",M:f"https://autopatchos.starrails.com/ifix/BetaLive/[\\w_-]+"}
	if A in[Q,R,S,T,U,V,W,X]:E=A4;H=f"{D}{B}&t=1713563129&uid=10004&language_type=3&platform_type=3&dispatch_seed={G}&channel_id=1&sub_channel_id=1&is_need_url=1&account_type=1&account_uid=307575403"
	elif A in[Y,Z,a,b]:E=A3;H=f"{D}{B}&t=1713563129&uid=10004&language_type=3&platform_type=1&dispatch_seed={G}&channel_id=1&sub_channel_id=1&is_need_url=1&account_type=1&account_uid=307575403"
	elif A in[c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u]:E=A1;H=f"{D}{B}.0&t=1713563129&uid=10004&language_type=3&platform_type=3&dispatch_seed={G}&channel_id=1&sub_channel_id=1&is_need_url=1&account_type=1&account_uid=307575403"
	elif A in[v,w,x,y]:E=A2;H=f"{D}{B}.0&t=1713563129&uid=10004&language_type=3&platform_type=1&dispatch_seed={G}&channel_id=1&sub_channel_id=1&is_need_url=1&account_type=1&account_uid=307575403"
	else:await C.message.reply_text(getTextMap(z));return
	try:
		O=requests.get(H);O.raise_for_status();A5=base64.b64decode(O.content);A6,A9=blackboxprotobuf.protobuf_to_json(A5)
		for(A7,A8)in E.items():P=re.findall(A8,A6);E[A7]=P[0]if P else'No URL found'
		with tempfile.NamedTemporaryFile('w+',suffix='.json',delete=False)as I:json.dump(E,I,indent=4);I.flush();I.seek(0);await C.message.reply_document(document=open(I.name,'rb'),filename='hotfix.json')
	except requests.exceptions.RequestException as N:await C.message.reply_text(f"Error making request: {N}")
	except Exception as N:await C.message.reply_text(f"Error: {N}")
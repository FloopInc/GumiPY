import requests,base64,json,re,tempfile,blackboxprotobuf
from telegram import Update
from telegram.ext import ContextTypes
from handler.register import isRegistered,isBanned,getTextMap
with open('data/dispatch.json')as config_file:config_data=json.load(config_file)
async def hotfix_command(update,context):
	A3='preDownloadUrl';A2='provideCurData';A1='ce_regress_asia';A0='ce_regress_eur';z='ce_regress_usa';y='cnprodsr';x='prodsrcn';w='srprodcn';v='cnsrprod';u='moprodsr';t='hkprodsr';s='twprodsr';r='chtprodsr';q='prodsrcht';p='srprodcht';o='chtsrprod';n='eurprodsr';m='prodsreur';l='srprodeur';k='eursrprod';j='usaprodsr';i='prodsrusa';h='srprodusa';g='usasrprod';f='asiaprodsr';e='prodsrasia';d='srprodasia';c='asiasrprod';b='cnbetasr';a='betacnsr';Z='srbetacn';Y='cnsrbeta';X='usabetasr';W='betausasr';V='srbetausa';U='usasrbeta';T='asiabetasr';S='betaasiasr';R='srbetaasia';Q='asiasrbeta';J='ifixUrl';I='luaUrl';H='exResourceUrl';G='assetBundleUrl';D=update;K=context.args
	if isBanned(D.message.from_user.id):await D.message.reply_text(isBanned(D.message.from_user.id),parse_mode='Markdown');return
	if not isRegistered(D.message.from_user.id):await D.message.reply_text(getTextMap('notRegistered'));return
	if len(K)<3:await D.message.reply_text(getTextMap('invalidReq'));return
	A=K[0].lower();C=K[1];F=K[2]
	if A in[Q,R,S,T]:B=config_data['beta_release01_asia']or config_data['beta_release02_asia']
	elif A in[U,V,W,X]:B=config_data['beta_release01_usa']or config_data['beta_release02_usa']
	elif A in[Y,Z,a,b]:B=config_data['beta_release01_cn']or config_data['beta_release02_cn']or config_data['beta_release03_cn']
	elif A in[c,d,e,f]:B=config_data['prod_official_asia']
	elif A in[g,h,i,j]:B=config_data['prod_official_usa']
	elif A in[k,l,m,n]:B=config_data['prod_official_eur']
	elif A in[o,p,q,r,s,t,u]:B=config_data['prod_official_cht']
	elif A in[v,w,x,y]:B=config_data['prod_gf_cn']
	elif A in['osce','oscecreation','ossrce']:B=config_data[z]or config_data[A0]or config_data[A1]
	elif A in['cnce','cncecreation','cnsrce']:B=config_data['ce_regress02_cn']
	elif A in['osceasia','ossrceasia','oscecreationasia']:B=config_data[A1]
	elif A in['osceusa','ossrceusa','oscecreationusa']:B=config_data[z]
	elif A in['osceeur','ossrceeur','oscecreationeur']:B=config_data[A0]
	else:await D.message.reply_text(getTextMap(A2));return
	A4={G:f"https://autopatchos.starrails.com/asb/V{C}Live/[\\w_-]+",H:f"https://autopatchos.starrails.com/design_data/V{C}Live/[\\w_-]+",I:f"https://autopatchos.starrails.com/lua/V{C}Live/[\\w_-]+",J:f"https://autopatchos.starrails.com/ifix/V{C}Live/[\\w_-]+",A3:f"https://autopatchos.starrails.com/pre_download/V2.7Live/[\\w_-]+"};A5={G:f"https://autopatchcn.bhsr.com/asb/V{C}Live/[\\w_-]+",H:f"https://autopatchcn.bhsr.com/design_data/V{C}Live/[\\w_-]+",I:f"https://autopatchcn.bhsr.com/lua/V{C}Live/[\\w_-]+",J:f"https://autopatchcn.bhsr.com/ifix/V{C}Live/[\\w_-]+",A3:f"https://autopatchcn.bhsr.com/pre_download/V2.7Live/[\\w_-]+"};A6={G:f"https://autopatchcn.bhsr.com/asb/BetaLive/[\\w_-]+",H:f"https://autopatchcn.bhsr.com/design_data/BetaLive/[\\w_-]+",I:f"https://autopatchcn.bhsr.com/lua/BetaLive/[\\w_-]+",J:f"https://autopatchcn.bhsr.com/ifix/BetaLive/[\\w_-]+"};A7={G:f"https://autopatchos.starrails.com/asb/BetaLive/[\\w_-]+",H:f"https://autopatchos.starrails.com/design_data/BetaLive/[\\w_-]+",I:f"https://autopatchos.starrails.com/lua/BetaLive/[\\w_-]+",J:f"https://autopatchos.starrails.com/ifix/BetaLive/[\\w_-]+"}
	if A in[Q,R,S,T,U,V,W,X]:E=A7;L=f"{B}{C}&t=1713563129&uid=10004&language_type=3&platform_type=3&dispatch_seed={F}&channel_id=1&sub_channel_id=1&is_need_url=1&account_type=1&account_uid=307575403"
	elif A in[Y,Z,a,b]:E=A6;L=f"{B}{C}&t=1713563129&uid=10004&language_type=3&platform_type=1&dispatch_seed={F}&channel_id=1&sub_channel_id=1&is_need_url=1&account_type=1&account_uid=307575403"
	elif A in[c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u]:E=A4;L=f"{B}{C}.0&t=1713563129&uid=10004&language_type=3&platform_type=3&dispatch_seed={F}&channel_id=1&sub_channel_id=1&is_need_url=1&account_type=1&account_uid=307575403"
	elif A in[v,w,x,y]:E=A5;L=f"{B}{C}.0&t=1713563129&uid=10004&language_type=3&platform_type=1&dispatch_seed={F}&channel_id=1&sub_channel_id=1&is_need_url=1&account_type=1&account_uid=307575403"
	else:await D.message.reply_text(getTextMap(A2));return
	try:
		O=requests.get(L);O.raise_for_status();A8=base64.b64decode(O.content);A9,AD=blackboxprotobuf.protobuf_to_json(A8)
		for(AA,AB)in E.items():P=re.findall(AB,A9);E[AA]=P[0]if P else'No URL found'
		AC=f"""Hotfix URLs for Honkai Star Rail Version {C}:

assetBundleUrl: {E[G]}

exResourceUrl: {E[H]}

luaUrl: {E[I]}

ifixUrl: {E[J]}

dispatchSeed: {F}

""";await D.message.reply_text(AC)
		with tempfile.NamedTemporaryFile('w+',suffix='.json',delete=False)as M:json.dump(E,M,indent=4);M.flush();M.seek(0);await D.message.reply_document(document=open(M.name,'rb'),filename='hotfix.json')
	except requests.exceptions.RequestException as N:await D.message.reply_text(f"Error making request: {N}")
	except Exception as N:await D.message.reply_text(f"Error: {N}")
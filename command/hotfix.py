import requests as Q,base64,json as R,re,tempfile as A9,blackboxprotobuf as AA
from telegram import Update
from telegram.ext import ContextTypes
from handler.register import isRegistered as AB,isBanned as S,getTextMap as L
with open('data/dispatch.json')as B:A=R.load(B)
async def C(update,context):
	A8='preDownloadUrl';A7='provideCurData';A6='ce_regress_asia';A5='ce_regress_eur';A4='ce_regress_usa';A3='cnprodsr';A2='prodsrcn';A1='srprodcn';A0='cnsrprod';z='moprodsr';y='hkprodsr';x='twprodsr';w='chtprodsr';v='prodsrcht';u='srprodcht';t='chtsrprod';s='eurprodsr';r='prodsreur';q='srprodeur';p='eursrprod';o='usaprodsr';n='prodsrusa';m='srprodusa';l='usasrprod';k='asiaprodsr';j='prodsrasia';i='srprodasia';h='asiasrprod';g='cnbetasr';f='betacnsr';e='srbetacn';d='cnsrbeta';c='usabetasr';b='betausasr';a='srbetausa';Z='usasrbeta';Y='asiabetasr';X='betaasiasr';W='srbetaasia';V='asiasrbeta';K='ifixUrl';J='luaUrl';I='exResourceUrl';H='assetBundleUrl';E=update;M=context.args
	if S(E.message.from_user.id):await E.message.reply_text(S(E.message.from_user.id),parse_mode='Markdown');return
	if not AB(E.message.from_user.id):await E.message.reply_text(L('notRegistered'));return
	if len(M)<3:await E.message.reply_text(L('invalidReq'));return
	B=M[0].lower();D=M[1];G=M[2]
	if B in[V,W,X,Y]:C=A['beta_release01_asia']or A['beta_release02_asia']
	elif B in[Z,a,b,c]:C=A['beta_release01_usa']or A['beta_release02_usa']
	elif B in[d,e,f,g]:C=A['beta_release01_cn']or A['beta_release02_cn']or A['beta_release03_cn']
	elif B in[h,i,j,k]:C=A['prod_official_asia']
	elif B in[l,m,n,o]:C=A['prod_official_usa']
	elif B in[p,q,r,s]:C=A['prod_official_eur']
	elif B in[t,u,v,w,x,y,z]:C=A['prod_official_cht']
	elif B in[A0,A1,A2,A3]:C=A['prod_gf_cn']
	elif B in['osce','oscecreation','ossrce']:C=A[A4]or A[A5]or A[A6]
	elif B in['cnce','cncecreation','cnsrce']:C=A['ce_regress02_cn']
	elif B in['osceasia','ossrceasia','oscecreationasia']:C=A[A6]
	elif B in['osceusa','ossrceusa','oscecreationusa']:C=A[A4]
	elif B in['osceeur','ossrceeur','oscecreationeur']:C=A[A5]
	else:await E.message.reply_text(L(A7));return
	AC={H:f"https://autopatchos.starrails.com/asb/V{D}Live/[\\w_-]+",I:f"https://autopatchos.starrails.com/design_data/V{D}Live/[\\w_-]+",J:f"https://autopatchos.starrails.com/lua/V{D}Live/[\\w_-]+",K:f"https://autopatchos.starrails.com/ifix/V{D}Live/[\\w_-]+",A8:f"https://autopatchos.starrails.com/pre_download/V2.7Live/[\\w_-]+"};AD={H:f"https://autopatchcn.bhsr.com/asb/V{D}Live/[\\w_-]+",I:f"https://autopatchcn.bhsr.com/design_data/V{D}Live/[\\w_-]+",J:f"https://autopatchcn.bhsr.com/lua/V{D}Live/[\\w_-]+",K:f"https://autopatchcn.bhsr.com/ifix/V{D}Live/[\\w_-]+",A8:f"https://autopatchcn.bhsr.com/pre_download/V2.7Live/[\\w_-]+"};AE={H:f"https://autopatchcn.bhsr.com/asb/BetaLive/[\\w_-]+",I:f"https://autopatchcn.bhsr.com/design_data/BetaLive/[\\w_-]+",J:f"https://autopatchcn.bhsr.com/lua/BetaLive/[\\w_-]+",K:f"https://autopatchcn.bhsr.com/ifix/BetaLive/[\\w_-]+"};AF={H:f"https://autopatchos.starrails.com/asb/BetaLive/[\\w_-]+",I:f"https://autopatchos.starrails.com/design_data/BetaLive/[\\w_-]+",J:f"https://autopatchos.starrails.com/lua/BetaLive/[\\w_-]+",K:f"https://autopatchos.starrails.com/ifix/BetaLive/[\\w_-]+"}
	if B in[V,W,X,Y,Z,a,b,c]:F=AF;N=f"{C}{D}&t=1713563129&uid=10004&language_type=3&platform_type=3&dispatch_seed={G}&channel_id=1&sub_channel_id=1&is_need_url=1&account_type=1&account_uid=307575403"
	elif B in[d,e,f,g]:F=AE;N=f"{C}{D}&t=1713563129&uid=10004&language_type=3&platform_type=1&dispatch_seed={G}&channel_id=1&sub_channel_id=1&is_need_url=1&account_type=1&account_uid=307575403"
	elif B in[h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]:F=AC;N=f"{C}{D}.0&t=1713563129&uid=10004&language_type=3&platform_type=3&dispatch_seed={G}&channel_id=1&sub_channel_id=1&is_need_url=1&account_type=1&account_uid=307575403"
	elif B in[A0,A1,A2,A3]:F=AD;N=f"{C}{D}.0&t=1713563129&uid=10004&language_type=3&platform_type=1&dispatch_seed={G}&channel_id=1&sub_channel_id=1&is_need_url=1&account_type=1&account_uid=307575403"
	else:await E.message.reply_text(L(A7));return
	try:
		T=Q.get(N);T.raise_for_status();AG=base64.b64decode(T.content);AH,AL=AA.protobuf_to_json(AG)
		for(AI,AJ)in F.items():U=re.findall(AJ,AH);F[AI]=U[0]if U else'No URL found'
		AK=f"""Hotfix URLs for Honkai Star Rail Version {D}:

assetBundleUrl: {F[H]}

exResourceUrl: {F[I]}

luaUrl: {F[J]}

ifixUrl: {F[K]}

dispatchSeed: {G}

""";await E.message.reply_text(AK)
		with A9.NamedTemporaryFile('w+',suffix='.json',delete=False)as O:R.dump(F,O,indent=4);O.flush();O.seek(0);await E.message.reply_document(document=open(O.name,'rb'),filename='hotfix.json')
	except Q.exceptions.RequestException as P:await E.message.reply_text(f"Error making request: {P}")
	except Exception as P:await E.message.reply_text(f"Error: {P}")
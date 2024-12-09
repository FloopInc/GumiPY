import requests
from telegram import Update
from telegram.ext import ContextTypes
from handler.register import isRegistered,isBanned,getTextMap
def format_package_info(pkg):A=pkg;return f"{A['url']} (Size: {int(A['size'])/1024**3:.2f}GB, Decompressed Size: {int(A['decompressed_size'])/1024**3:.2f}GB)"
def loadPackage(url):
	U='pre_download';T='patches';M='version';G='language';F='audio_pkgs';E='game_pkgs';D='major';C='main';A='\n';V=requests.get(url);N=V.json()
	if N['retcode']!=0:return'Error: Unable to fetch game data.'
	B=N['data']['game_packages'][0];W=B[C][D][M];X=B[C][D][E];Y=B[C][D][F];O=B[C][T];H=B.get(U,{}).get(D,{});Z=B.get(U,{});a=A.join([format_package_info(A)for A in X]);b=A.join([f"   - Language {A[G]}: {format_package_info(A)}"for A in Y]);I=''
	if O:
		for J in O:c=J[M];d=A.join([format_package_info(A)for A in J[E]]);e=A.join([f"    - Language {A[G]}: {format_package_info(A)}"for A in J[F]]);I+=f"""
- Version {c}:
  Game Packages:
{d}
  Audio Packages:
{e}
"""
	f=f"""
Version: {W}

Full Game Packages:
{a}

Full Audio Packages:
{b}

Patches:
{I if I else"No patches available."}
""".strip();P=None
	if H:
		Q=A.join([format_package_info(A)for A in H.get(E,[])]);R=A.join([f"   - Language {A[G]}: {format_package_info(A)}"for A in H.get(F,[])]);K='';S=Z.get(T,[])
		if S:
			for L in S:g=L[M];h=A.join([format_package_info(A)for A in L[E]]);i=A.join([f"    - Language {A[G]}: {format_package_info(A)}"for A in L[F]]);K+=f"""
- Version {g}:
  Game Packages:
{h}
  Audio Packages:
{i}
"""
		P=f"""
Pre-download Game Packages:
{Q if Q else"No pre-download Game Packages available"}

Pre-download Audio Packages:
{R if R else"No pre-download audio packages available."}

Pre-download Patches:
{K if K else"No pre-download patches available."}
""".strip()
	return f,P
async def package_command(update,context):
	A=update;B=A.message.from_user.id;E=context.args
	if isBanned(B):await A.message.reply_text(isBanned(B),parse_mode='Markdown');return
	if not isRegistered(B):await A.message.reply_text(getTextMap('notRegistered'));return
	if len(E)<1:await A.message.reply_text('Please provide a package name.');return
	C=E[0].lower()
	if C in['gi','genshin','genshinimpact','yuanshen','hk4e']:D=f"https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getGamePackages?game_ids[]=gopR6Cufr3&launcher_id=VYTpXlbWo8"
	elif C in['starrail','bhsr','sr','honkaistarrail','hsr','hkrpg']:D=f"https://sg-hyp-api.hoyoverse.com/hyp/hyp-connect/api/getGamePackages?game_ids%5B%5D=4ziysqXOQ8&launcher_id=VYTpXlbWo8"
	else:await A.message.reply_text('Invalid package name. Please provide a valid package name.');return
	G,F=loadPackage(D);await A.message.reply_text(G)
	if F:await A.message.reply_text(F)
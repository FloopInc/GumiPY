import json
from telegram import Update
from telegram.ext import ContextTypes
import os
from handler.register import isRegistered,isBanned,getTextMap
HOTFIX_JSON_PATH='data/hotfix.json'
def load_hotfix_data():
	if not os.path.isfile(HOTFIX_JSON_PATH):return
	with open(HOTFIX_JSON_PATH,'r')as A:return json.load(A)
async def hotfix_command(update,context):
	C='No URLs found.';B=update;D=B.message.from_user.id
	if isBanned(D):await B.message.reply_text(getTextMap('isBanned'));return
	if not isRegistered(D):await B.message.reply_text(getTextMap('notRegistered'));return
	A=load_hotfix_data()
	if A is None:await B.message.reply_text('Hotfix data not found.');return
	E=f"""Hotfix URLs for Honkai Star Rail Version {A.get("version","No version found.")}:

dispatch seed: {A.get("dispatchSeed","No seed found.")}

assetBundleUrl:

 {A.get("assetBundleUrl",C)}

exResourceUrl:

 {A.get("exResourceUrl",C)}

luaUrl:

 {A.get("luaUrl",C)}

ifixUrl:

 {A.get("ifixUrl",C)}

last update: {A.get("lastUpdate","No Date found")}
""";await B.message.reply_text(E)
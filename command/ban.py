from telegram import Update
from telegram.ext import ContextTypes
import json
from auth.register import is_banned,ban
with open('config.json')as config_file:config_data=json.load(config_file);ownerID=config_data['Owner']
async def ban_command(update,context):
	A=update;C=A.message.from_user.id;D=A.message.text.strip();B=D.split(' ')
	if is_banned(A.message.from_user.id):await A.message.reply_text("Oh cmon you are already banned from using this bot and you're still trying ban someone/yourself?.  If you believe this is a mistake, please contact support @ozmoon1337.");return
	if not ownerID==C:await A.message.reply_text('You are not authorized to use this command.');return
	if len(B)==1:await A.message.reply_text('Please provide a user ID to ban.');return
	E=B[1];F=ban(E);await A.message.reply_text(F['message'])
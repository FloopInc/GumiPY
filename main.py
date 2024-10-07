_C='waiting_for_image'
_B='notRegistered'
_A='Markdown'
from typing import Final
from telegram import Update
from telegram.ext import Application,CommandHandler,ContextTypes,MessageHandler,filters
import json,os,time,psutil,requests,tempfile
from command import setacc,editacc,help,start,check,ban,unban,hotfix,info,gacha,give,store,sb,mods,redeemcode,dailyquest
from handler.broadcast import radio_command
from handler.event import getEventMessage,event_command
from handler.DailyLogin import dailylogin_command
from handler.register import searchJson,isRegistered,isBanned,getTextMap,loadOwner,register_command
from handler import textmap
from colorama import Fore,Style
from PIL import Image
from rembg import remove
with open('data/config.json')as config_file:config_data=json.load(config_file);botToken=config_data['TOKEN'];botUsername=config_data['username']
TOKEN=botToken
BOT_USERNAME=botUsername
def linkLargeJson():
	B='https://raw.githubusercontent.com/PutraZC/HSR_Data/refs/heads/main/TextMapEN.json'
	try:A=requests.get(B);A.raise_for_status();return A.json()
	except requests.exceptions.RequestException as C:print(f"[{int(time.time())%86400//3600:02d}:{int(time.time())%3600//60:02d}:{time.time()%60:02.0f}] [{Fore.RED}ERROR{Style.RESET_ALL}] Error fetching JSON From GitHub: {C}")
def handle_response(text):
	A=text.lower()
	if'hello'in A:return'Hello there ! How can I help you today ? contact moderators for help /mods'
	return'I am sorry, I do not understand.'
async def handle_message(update,context):
	A=update;D=A.message.chat.type;B=A.message.text;print(f"[{int(time.time())%86400//3600:02d}:{int(time.time())%3600//60:02d}:{time.time()%60:02.0f}] [{Fore.YELLOW}MESSAGE{Style.RESET_ALL}] Received message from user ({A.message.chat.id}) in {D}: {B}")
	if D=='group':
		if isBanned(A.message.from_user.id):await A.message.reply_text(isBanned(A.message.from_user.id),parse_mode=_A);return
		if not isRegistered(A.message.from_user.id):await A.message.reply_text(getTextMap(_B));return
		if BOT_USERNAME in B:E=B.replace(BOT_USERNAME,'').strip();C=handle_response(E)
		else:return
	else:
		if isBanned(A.message.from_user.id):await A.message.reply_text(isBanned(A.message.from_user.id),parse_mode=_A);return
		if not isRegistered(A.message.from_user.id):await A.message.reply_text(getTextMap(_B));return
		C=handle_response(B)
	print(f"[{int(time.time())%86400//3600:02d}:{int(time.time())%3600//60:02d}:{time.time()%60:02.0f}] [{Fore.GREEN}BOT{Style.RESET_ALL}] Response:",C);await A.message.reply_text(C)
async def ping_command(update,context):
	A=update;B=A.message.from_user.id;J=loadOwner()
	if isBanned(B):await A.message.reply_text(isBanned(B),parse_mode=_A);return
	if not isRegistered(B):await A.message.reply_text(getTextMap(_B));return
	K=time.time();await A.message.reply_text('Requesting...');L=time.time();D=int((L-K)*1000)
	if B==J:E=psutil.virtual_memory();M=E.total//(1024*1024);N=E.used//(1024*1024);O=f"Memory Usage: {N}MB/{M}MB";P=psutil.cpu_percent(interval=1);Q=f"CPU Usage: {P}%";R=psutil.boot_time();F=time.time()-R;G=f"Uptime: {int(F//3600)}h {int(F%3600//60)}m";H='user/';S=len([A for A in os.listdir(H)if os.path.isfile(os.path.join(H,A))]);T=f"Total Registered Users: {S}";C=f"""Server Status:

Ping: ({D} ms)
{O}
{Q}
{G}
{T}"""
	else:C=f"Pong! ({D} ms) \n{G}"
	I=getEventMessage()
	if I:C+=f"\n\n{I}"
	await A.message.reply_text(C)
async def rules_command(update,context):
	with open('rules.txt','r')as A:B=A.read()
	await update.message.reply_text(B,parse_mode=_A)
async def search_command(update,context):
	A=update;B=A.message.from_user.id;G=A.message.text.strip();C=G.split(' ',1)
	if isBanned(B):await A.message.reply_text(isBanned(B),parse_mode=_A);return
	if not isRegistered(B):await A.message.reply_text(getTextMap(_B));return
	if len(C)<2:await A.message.reply_text('Please provide a keyword to search.');return
	D=C[1];E=linkLargeJson()
	if E:
		F,H=searchJson(D,E)
		if F:I=f"HSR (2.5.54) Found {H} unique result(s) for '{D}':\n\n"+'\n\n'.join(F);await A.message.reply_text(I)
		else:await A.message.reply_text(getTextMap('noResultFound'))
	else:await A.message.reply_text('Failed to fetch the data from the source.')
def remove_background(input_image_path,output_image_path):A=Image.open(input_image_path);B=remove(A);B.save(output_image_path)
async def removebg_command(update,context):
	A=update;B=A.message.from_user.id
	if isBanned(B):await A.message.reply_text(isBanned(B),parse_mode=_A);return
	if not isRegistered(B):await A.message.reply_text(getTextMap(_B));return
	await A.message.reply_text("Please upload an image, and I'll remove the background!");context.user_data[B]=_C
async def handle_image(update,context):
	B=context;A=update;C=A.message.from_user.id
	if B.user_data.get(C)==_C:
		await A.message.reply_text('Processing your image... This might take a few seconds.');G=A.message.photo[-1];H=await B.bot.get_file(G.file_id)
		with tempfile.TemporaryDirectory()as D:
			E=os.path.join(D,'input_image.png');F=os.path.join(D,'output_image.png');await H.download_to_drive(E)
			try:
				remove_background(E,F)
				with open(F,'rb')as I:await A.message.reply_photo(photo=I)
				await A.message.reply_text("Done! Here's your image with the background removed.")
			except Exception as J:await A.message.reply_text(getTextMap('errorRequest')+str(J))
		B.user_data[C]=None
	else:await A.message.reply_text('Please run /removebg first and then upload an image.')
async def error(update,context):print(f"Update {update} caused error {context.error}")
if __name__=='__main__':print(f"[{int(time.time())%86400//3600:02d}:{int(time.time())%3600//60:02d}:{time.time()%60:02.0f}] [{Fore.BLUE}INFO{Style.RESET_ALL}] Starting bot...");app=Application.builder().token(TOKEN).build();app.add_handler(CommandHandler('start',start.start_command));app.add_handler(CommandHandler('help',help.help_command));app.add_handler(CommandHandler('check',check.check_version));app.add_handler(CommandHandler('ban',ban.ban_command));app.add_handler(CommandHandler('unban',unban.unban_command));app.add_handler(CommandHandler('hotfix',hotfix.hotfix_command));app.add_handler(CommandHandler('info',info.info_command));app.add_handler(CommandHandler('gacha',gacha.gacha_command));app.add_handler(CommandHandler('give',give.give_command));app.add_handler(CommandHandler('store',store.store_command));app.add_handler(CommandHandler('sb',sb.sb_command));app.add_handler(CommandHandler('mods',mods.mods_command));app.add_handler(CommandHandler('setacc',setacc.setacc_command));app.add_handler(CommandHandler('editacc',editacc.editacc_command));app.add_handler(CommandHandler('redeemcode',redeemcode.redeemcode_command));app.add_handler(CommandHandler('textmapdiff',textmap.textmapdiff_command));app.add_handler(CommandHandler('dailyquest',dailyquest.dailyquest_command));app.add_handler(CommandHandler('event',event_command));app.add_handler(CommandHandler('rules',rules_command));app.add_handler(CommandHandler('radio',radio_command));app.add_handler(CommandHandler('dailylogin',dailylogin_command));app.add_handler(CommandHandler('ping',ping_command));app.add_handler(CommandHandler('search',search_command));app.add_handler(CommandHandler('register',register_command));app.add_handler(CommandHandler('removebg',removebg_command));app.add_handler(MessageHandler(filters.PHOTO,handle_image));app.add_handler(MessageHandler(filters.TEXT&filters.Regex('^https?://'),textmap.handle_url));app.add_handler(MessageHandler(filters.TEXT&~filters.COMMAND,handle_message));app.add_error_handler(error);print(f"[{int(time.time())%86400//3600:02d}:{int(time.time())%3600//60:02d}:{time.time()%60:02.0f}] [{Fore.BLUE}INFO{Style.RESET_ALL}] Polling bot...");app.run_polling(poll_interval=5)
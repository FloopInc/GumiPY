import json,os,tempfile,requests
from telegram import Update
from telegram.ext import ContextTypes
from handler.register import isRegistered, isBanned, getTextMap

def load_hotfix():
    url = f'https://raw.githubusercontent.com/PutraZC/HSR_Data/refs/heads/main/hotfix.json'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

async def hotfix_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if isBanned(user_id):
        await update.message.reply_text(isBanned(user_id), parse_mode='Markdown')
        return
    
    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return

    hotfix_data = load_hotfix()
    if hotfix_data is None:
        await update.message.reply_text('Hotfix data not found.')
        return

    response = (
        f"Hotfix URLs for Honkai Star Rail Version {hotfix_data.get('version', 'No version found.')}:\n\n"
        f"dispatch seed: {hotfix_data.get('dispatchSeed', 'No seed found.')}\n\n"
        f"last update: {hotfix_data.get('lastUpdate', 'No Date found')}\n"
    )

    await update.message.reply_text(response)

    file_data = {
        "assetBundleUrl": hotfix_data.get("assetBundleUrl"),
        "exResourceUrl": hotfix_data.get("exResourceUrl"),
        "luaUrl": hotfix_data.get("luaUrl"),
        "ifixUrl": hotfix_data.get("ifixUrl"),
        "preDownloadUrl": hotfix_data.get("preDownloadUrl"),
        "customMdkResVersion": hotfix_data.get("customMdkResVersion"),
        "customIfixVersion": hotfix_data.get("customIfixVersion")
    }

    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json') as temp_file:
        json.dump(file_data, temp_file, indent=4)
        temp_file_path = temp_file.name

    await update.message.reply_document(document=open(temp_file_path, 'rb'), filename="hotfix.json")
    
    os.remove(temp_file_path)
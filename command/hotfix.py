import json
from telegram import Update
from telegram.ext import ContextTypes
import os

from handler.register import isRegistered, isBanned, getTextMap

HOTFIX_JSON_PATH = 'data/hotfix.json'

def loadHotfixData():
    if not os.path.isfile(HOTFIX_JSON_PATH):
        return None
    with open(HOTFIX_JSON_PATH, 'r') as file:
        return json.load(file)

async def hotfix_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if isBanned(user_id):
        await update.message.reply_text(getTextMap("isBanned"))
        return
    
    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return

    hotfix_data = loadHotfixData()
    if hotfix_data is None:
        await update.message.reply_text('Hotfix data not found.')
        return

    response = (
        f"Hotfix URLs for Honkai Star Rail Version {hotfix_data.get('version', 'No version found.')}:\n\n"
        f"dispatch seed: {hotfix_data.get('dispatchSeed', 'No seed found.')}\n\n"
        f"assetBundleUrl:\n\n {hotfix_data.get('assetBundleUrl', 'No URLs found.')}\n\n"
        f"exResourceUrl:\n\n {hotfix_data.get('exResourceUrl', 'No URLs found.')}\n\n"
        f"luaUrl:\n\n {hotfix_data.get('luaUrl', 'No URLs found.')}\n\n"
        f"ifixUrl:\n\n {hotfix_data.get('ifixUrl', 'No URLs found.')}\n\n"
        f"last update: {hotfix_data.get('lastUpdate', 'No Date found')}\n"
    )

    await update.message.reply_text(response)

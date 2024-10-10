from telegram import Update
from telegram.ext import CallbackContext
from handler.register import loadUserStatus, saveUserStatus, getTextMap

async def mods_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_status = loadUserStatus()
    args = context.args

    if str(user_id) in user_status and user_status[str(user_id) ].get("isModerator", False):
        if len(args) > 0 and args[0].lower() == "hide":
            current_status = user_status[str(user_id) ].get("isHidden", False)
            user_status[str(user_id)]["isHidden"] = not current_status
            saveUserStatus(user_status)

            if user_status[str(user_id)]["isHidden"]:
                await update.message.reply_text(getTextMap("modHide"))
            else: 
                await update.message.reply_text(getTextMap("modShow"))
            return
        
    mods_list = []
    for mod_id, status in user_status.items():
        if status.get("isModerator", False) and not status.get("isHidden", False):
            username = "@" + status.get("username", "Unknown")
            mods_list.append(username)

    if not mods_list:
        mods_message = "Moderator Available List: (All are hidden/not available)"
        mods_message += ("\n\n" + getTextMap("mods"))
        await update.message.reply_text(mods_message)
    else:
        mods_message = "Moderator Available List: " + ", ".join(mods_list)
        mods_message += ("\n\n" + getTextMap("mods"))
        await update.message.reply_text(mods_message)

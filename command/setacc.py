from telegram import Update
from telegram.ext import CallbackContext
from handler.register import loadUserStatus, saveUserStatus, getTextMap, loadOwner

async def setacc_command(update: Update, context: CallbackContext):
    ownerID = loadOwner()
    
    if not ownerID == update.message.from_user.id:
        await update.message.reply_text(getTextMap("onlyOwner1"))
        return
    if len(context.args) < 2:
        await update.message.reply_text(getTextMap("setUsage"))
        return

    target_user = context.args[0]  
    statusToEdit = context.args[1].lower() 
    
    userStats = loadUserStatus()

    target_id = None
    for user_id, status in userStats.items():
        if str(user_id) == target_user or status.get("username", "").lower() == target_user.lower():
            target_id = user_id
            break

    if target_id is None:
        await update.message.reply_text(getTextMap("notFound"))
        return
    
    if statusToEdit == "moderator" or statusToEdit == "mod": 
        current_value = userStats[target_id].get("isModerator", False)
        userStats[target_id]["isModerator"] = not current_value
        status_message = f"Set Moderator for {target_user} to {'True' if not current_value else 'False'}."
    elif statusToEdit == "hide" or statusToEdit == "hidden":
        current_value = userStats[target_id].get("isHidden", False)
        userStats[target_id]["isHidden"] = not current_value
        status_message = f"Set Hidden for {target_user} to {'True' if not current_value else 'False'}."
    elif statusToEdit == "ban":
        current_value = userStats[target_id].get("isBanned", False)
        userStats[target_id]["isBanned"] = not current_value
        status_message = f"Set Banned for {target_user} to {'True' if not current_value else 'False'}."
    elif statusToEdit == "register" or statusToEdit == "regist" or statusToEdit == "registered" or statusToEdit == "reg":
        current_value = userStats[target_id].get("registered", False)
        userStats[target_id]["registered"] = not current_value
        status_message = f"Set Registered for {target_user} to {'True' if not current_value else 'False'}."
    elif statusToEdit == "radio":
        current_value = userStats[target_id].get("isRadio", False)
        userStats[target_id]["isRadio"] = not current_value
        status_message = f"Set Radio for {target_user} to {'True' if not current_value else 'False'}."
    elif statusToEdit == "resetban" or statusToEdit == "unban":
        current_value = userStats[target_id].get("banExpires", 0)
        if current_value == 0:
            status_message = f"{target_user} is not banned."
            return
        userStats[target_id]["banExpires"] = 0
        status_message = f"Reset Ban for {target_user}."
    else:
        await update.message.reply_text(getTextMap("statsValue"))
        return

    saveUserStatus(userStats)
    await update.message.reply_text(status_message)

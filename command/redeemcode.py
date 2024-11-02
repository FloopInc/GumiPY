from telegram import Update
from telegram.ext import CallbackContext
from handler.register import getTextMap, loadOwner, isMod, loadUserProfile, saveUserProfile
from handler.profile import loadRedeemCode, saveRedeemCode, deleteRedeemCode
from handler.economy import loadItems

async def redeemcode_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_profile = loadUserProfile(user_id)
    items = loadItems()
    ownerId = loadOwner()

    args = context.args

    if len(args) == 0:
        await update.message.reply_text(getTextMap("redeemUsage"))
        return
    
    if user_id == ownerId or isMod(user_id):
        if args[0].lower() == "create" or args[0].lower() == "c":
            if len(args) < 4:
                await update.message.reply_text(getTextMap("redeemCreateUsage"))
                return

            code = args[1]
            max_redeem = int(args[2])

            items_to_add = {}
            for item_arg in args[3:]:
                try:
                    item_id, amount = item_arg.split(":")
                    item_id = int(item_id)
                    amount = int(amount)
                    if str(item_id) not in items:
                        await update.message.reply_text(f"Invalid item ID: {item_id}")
                        return
                    items_to_add[f"itemId{len(items_to_add) + 1}"] = {str(item_id): amount}
                except ValueError:
                    await update.message.reply_text(f"Invalid format for item: {item_arg}")
                    return

            redeem_data = {
                "count": max_redeem,
                **items_to_add,
                "blacklist": []
            }
            saveRedeemCode(code, redeem_data)
            await update.message.reply_text(f"Redeem code '{code}' created successfully!")
            return

    code = args[0]
    redeem_data = loadRedeemCode(code)

    if not redeem_data:
        await update.message.reply_text("Invalid redeem code.")
        return

    if redeem_data["count"] <= 0:
        deleteRedeemCode(code)
        await update.message.reply_text("This redeem code is no longer available.")
        return

    if "blacklist" in redeem_data and user_id in redeem_data["blacklist"]:
        await update.message.reply_text("You have already redeemed this code.")
        return
    
    redeemed_items_message = "Successfully redeemed:\n"

    for item_key, item_info in redeem_data.items():
        if item_key.startswith("itemId"):
            for item_id, amount in item_info.items():
                user_profile.setdefault(item_id, 0)
                user_profile[item_id] += amount
                item_name = items[str(item_id)]["name"]
                item_logo = items[str(item_id)]["logo"]
                redeemed_items_message += f"{item_logo} {item_name}: {amount}\n"

    redeem_data["count"] -= 1

    if redeem_data["count"] <= 0:
        deleteRedeemCode(code)

    redeem_data.setdefault("blacklist", []).append(user_id)

    saveUserProfile(user_id, user_profile)
    saveRedeemCode(code, redeem_data)

    await update.message.reply_text(redeemed_items_message)

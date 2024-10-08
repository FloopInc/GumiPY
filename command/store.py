from telegram import Update
from telegram.ext import CallbackContext
from handler.event import getEventMessage
from handler.store import getStoreItems, buyItem, sellItem
from handler.register import isRegistered, isBanned, getTextMap

async def store_command(update: Update, context: CallbackContext):
    store_items = getStoreItems()
    args = context.args

    if isBanned(update.message.from_user.id):
        await update.message.reply_text(isBanned(update.message.from_user.id), parse_mode="Markdown")
        return
    
    if not isRegistered(update.message.from_user.id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
    
    if args:
        action = args[0].lower()

        if action == "buy":
            if len(args) >= 2:
                if args[-1].isdigit():  
                    item_name = " ".join(args[1:-1])  
                    quantity = int(args[-1])  
                else:  
                    item_name = " ".join(args[1:])
                    quantity = 1
                result = buyItem(update.message.from_user.id, item_name, quantity)
                await update.message.reply_text(result["message"])
            return

        elif action == "sell":
            if len(args) >= 2:
                if args[-1].isdigit():  
                    item_name = " ".join(args[1:-1])  
                    quantity = int(args[-1])  
                else:  
                    item_name = " ".join(args[1:])
                    quantity = 1
                result = sellItem(update.message.from_user.id, item_name, quantity)
                await update.message.reply_text(result["message"])
            return
    
    if not store_items:
        await update.message.reply_text("No items available in the store.")
        return
    
    store_message = "🛒 Welcome to the Store! Here are the available items:\n\n"

    event_message = getEventMessage()
    if event_message:
        store_message += event_message + "\n\n"
    
    for item in store_items:
        store_message += f"{item['logo']} {item['name']}\n"
        store_message += f"Price: {item['buy']} 💵 Money\n"
        store_message += f"Sell: {item['sell']} 💵 Money\n"
        store_message += f"{item['stock_message']}\n\n"
    
    await update.message.reply_text(store_message)

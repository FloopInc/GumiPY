import json,time,colorama
from telegram import Update
from telegram.ext import CallbackContext
from handler.register import getTextMap, loadOwner, isBanned, isRegistered
from handler.economy import loadItems,saveItems
def loadEventData():
    with open('data/Event.json', 'r') as f:
        return json.load(f)

def saveEventData(event_data):
    with open('data/Event.json', 'w') as f:
        json.dump(event_data, f, indent=4)

def toggleCrownDay():
    event_data = loadEventData()
    items = loadItems()
    
    # Toggle the event
    event_status = not event_data.get("CrownDay", False)
    event_data["CrownDay"] = event_status

    # Update the Crown Title item
    for item_id, item_data in items.items():
        if item_data["name"] == "Crown Title":
            item_data["untradeable"] = not event_status
            break

    # Save the updated event and items data
    saveEventData(event_data)
    saveItems(items)

    return {"event": "CrownDay", "status": event_status}
    
def toggleBroadcastDay():
    event_data = loadEventData()
    items = loadItems()
    
    # Toggle the event
    event_status = not event_data.get("BroadcastDay", False)
    event_data["BroadcastDay"] = event_status

    for item_id, item_data in items.items():
        if item_data["name"] == "Megaphone":
            item_data["untradeable"] = not event_status
            item_data["buy"] = int(item_data["buy"] / 3) if event_status else int(item_data["buy"] * 3)
            item_data["sell"] = int(item_data["sell"] / 2) if event_status else int(item_data["sell"] * 2)
            break

    # Save the updated event and items data
    saveEventData(event_data)
    saveItems(items)

    return {"event": "BroadcastDay", "status": event_status}

def toggleWeeklyLogin():
    event_data = loadEventData()
    event_status = not event_data.get("WeeklyLogin", False)
    event_data["WeeklyLogin"] = event_status

    saveEventData(event_data)
    return {"event": "WeeklyLogin", "status": event_status}

def getEventMessage():
    events = loadEventData()
    event_messages = []

    if events.get("CrownDay"):
        event_messages.append(getTextMap("CrownDay"))

    if events.get("BroadcastDay"):
        event_messages.append(getTextMap("BroadcastDay"))

    if events.get("WeeklyLogin"):
        event_messages.append(getTextMap("WeeklyLogin"))

    return "\n\n".join(event_messages) if event_messages else None

async def event_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    ownerId = loadOwner()

    if not ownerId == user_id:
        await update.message.reply_text(getTextMap("onlyOwner"))
        return
        
    if isBanned(user_id):
        await update.message.reply_text(isBanned(user_id), parse_mode="Markdown")
        return

    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
    
    args = context.args

    if len(args) == 0:
        await update.message.reply_text("Please specify an event name. eg. /event crownday")
        return
    
    event_name = args[0].lower()

    if event_name == "crownday" or event_name == "crown":
        result = toggleCrownDay()
        if result["status"]:
            await update.message.reply_text("CrownDay event is now active! Crown Title is now tradeable.")
            print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] {user_id}/{update.message.from_user.username} has turned on the CrownDay event!.")
        else:
            print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] {user_id}/{update.message.from_user.username} has turned off the CrownDay event!.")
            await update.message.reply_text("CrownDay event is now inactive! Crown Title is back to being untradeable.")
        return
    elif event_name == "weeklylogin" or event_name == "weekly" or event_name == "login":
        result = toggleWeeklyLogin()
        if result["status"]:
            await update.message.reply_text("WeeklyLogin event is now active! Users Can now claim /dailylogin rewards.")
            print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] {user_id}/{update.message.from_user.username} has turned on the WeeklyLogin event!.")
        else:
            await update.message.reply_text("WeeklyLogin event is now inactive! Users Can no longer claim /dailylogin rewards.")
            print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] {user_id}/{update.message.from_user.username} has turned off the WeeklyLogin event!.")
        return
    elif event_name == "broadcastday" or event_name == "megaphone" or event_name == "broadcast" or event_name == "bc":
        result = toggleBroadcastDay()
        if result["status"]:
            print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] {user_id}/{update.message.from_user.username} has turned On the BroadcastDay event!.")
            await update.message.reply_text("BroadcastDay event is now active! Megaphone is now tradeable.")
        else:
            await update.message.reply_text("BroadcastDay event is now inactive! Megaphone is back to being untradeable.")
            print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] {user_id}/{update.message.from_user.username} has turned off the BroadcastDay event!.")
        return

    await update.message.reply_text(f"Event '{event_name}' not found.")
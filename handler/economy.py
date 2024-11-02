import os,json,random,colorama,time
def loadItems():
    with open('data/items.json', 'r') as f:
        return json.load(f)

def saveItems(items):
    with open('data/items.json', 'w') as f:
        json.dump(items, f, indent=4)
        
def loadItemMapping():
    items = loadItems()
    return {item["name"]: item_id for item_id, item in items.items()}

def loadGachaConfig():
    with open('data/GachaConfig.json', 'r') as f:
        return json.load(f) 

def usercd(user_id: int, username: str):
    userdir = 'user/'
    user_filepath = os.path.join(userdir, f'{user_id}.json')
    
    if not os.path.exists(userdir):
        os.makedirs(userdir)
    
    items = loadItems()
    default_items = {item_id: 0 for item_id in items.keys()}
    
    if os.path.exists(user_filepath):
        with open(user_filepath, 'r') as f:
            userData = json.load(f)
    else:
        userData = {}
    
    userData.setdefault("name", username)
    userData.setdefault("dailyLogin", 0)
    userData.setdefault("lastClaimTime", 0)
    userData.setdefault("logs", [])
    userData.setdefault("banReason", "")

    userData.setdefault("1000", 5000)
    for item_id, quantity in default_items.items():
        userData.setdefault(item_id, quantity)
    
    with open(user_filepath, 'w') as f:
        json.dump(userData, f, indent=4)

def performGacha(user_id: int, boxIdorName: str = None):
    items = loadItems()
    gacha_config = loadGachaConfig()
    
    boxNameToIds = {
        "Mystery Box": "1007",
        "Super Mystery Box": "1008"
    }
    
    user_filepath = f'user/{user_id}.json'
    
    if not os.path.exists(user_filepath):
        return {"message": "User data not found."}
    
    with open(user_filepath, 'r') as f:
        user_data = json.load(f)
    
    if boxIdorName:
        boxId = boxIdorName
        if boxId in boxNameToIds.values():
            pass
        elif boxId in boxNameToIds:
            boxId = boxNameToIds[boxId]
        else:
            return {"message": "Invalid box ID or name."}
    else:
        if "1007" in user_data and user_data["1007"] > 0:
            boxId = "1007"
        elif "1008" in user_data and user_data["1008"] > 0:
            boxId = "1008"
        else:
            return {"message": "You don't have any gacha items to perform."}
    
    if boxId not in user_data or user_data[boxId] <= 0:
        return {"message": "You don't have this item to perform gacha."}
    
    user_data[boxId] -= 1
    if user_data[boxId] <= 0:
        user_data[boxId] = 0
        
    with open(user_filepath, 'w') as f:
        json.dump(user_data, f, indent=4)
    
    if boxId not in gacha_config:
        return {"message": "Invalid box ID."}
    
    boxConfig = gacha_config[boxId]
    
    if random.random() < 0.7:
        chosen_category = "noob_item"
    else:
        chosen_category = "rare_item"
    
    chosen_items = boxConfig[chosen_category]
    chosen_item = random.choice(chosen_items)
    
    user_data.setdefault(chosen_item["item_id"], 0)
    user_data[chosen_item["item_id"]] += chosen_item["quantity"]
    
    with open(user_filepath, 'w') as f:
        json.dump(user_data, f, indent=4)
    
    item_details = loadItems()
    reward_message = f"Congratulations! From Gacha {item_details[boxId]['logo']} {item_details[boxId]['name']} You've received the following reward:\n"
    reward_message += f"{item_details[chosen_item['item_id']]['logo']} {item_details[chosen_item['item_id']]['name']} x{chosen_item['quantity']}"
    
    return {"message": reward_message}

def giveItem(from_user_id: int, toUserName: str, item_name: str, quantity: int):
    item_mapping = loadItemMapping()
    item_id = item_mapping.get(item_name)
    
    if not item_id:
        return {"message": f"Item '{item_name}' not found."}
    
    UserDir = 'user/'
    fromUserFilepath = os.path.join(UserDir, f'{from_user_id}.json')
    
    if not os.path.exists(fromUserFilepath):
        return {"message": "Sender's data not found."}
    
    with open(fromUserFilepath, 'r') as f:
        fromUserData = json.load(f)

    if item_id not in fromUserData or fromUserData[item_id] < quantity:
        return {"message": "Insufficient quantity to give."}
    
    fromUserData[item_id] -= quantity
    if fromUserData[item_id] <= 0:
        fromUserData[item_id] = 0
    
    with open(fromUserFilepath, 'w') as f:
        json.dump(fromUserData, f, indent=4)
    
    recipient_user_file = None
    for filename in os.listdir(UserDir):
        if filename.endswith('.json'):
            with open(os.path.join(UserDir, filename), 'r') as f:
                user_data = json.load(f)
                if user_data.get("name") == toUserName:
                    recipient_user_file = os.path.join(UserDir, filename)
                    break
    
    if not recipient_user_file:
        return {"message": "Recipient not found."}
    
    with open(recipient_user_file, 'r') as f:
        to_user_data = json.load(f)
    
    to_user_data.setdefault(item_id, 0)
    to_user_data[item_id] += quantity
    
    with open(recipient_user_file, 'w') as f:
        json.dump(to_user_data, f, indent=4)
    
    print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] {from_user_id}/{fromUserData['name']} gave {quantity} of item {item_name} to {toUserName}.")
    
    return {"message": f"Successfully gave {quantity} of item {item_name} to {toUserName}."}


def modGiveItem(from_user_id: int, toUserName: str, item_name: str, quantity: int):
    itemMapping = loadItemMapping()
    item_id = itemMapping.get(item_name)

    if not item_id:
        return {"message": f"Item '{item_id}' not found."}
    
    UserDir = 'user/'
    
    recipient_user_file = None
    for filename in os.listdir(UserDir):
        if filename.endswith('.json'):
            with open(os.path.join(UserDir, filename), 'r') as f:
                user_data = json.load(f)
                if user_data.get("name") == toUserName:
                    recipient_user_file = os.path.join(UserDir, filename)
                    break
    
    if not recipient_user_file:
        return {"message": "Recipient not found."}
    
    with open(recipient_user_file, 'r') as f:
        to_user_data = json.load(f)
    
    to_user_data.setdefault(item_id, 0)
    to_user_data[item_id] += quantity
    
    with open(recipient_user_file, 'w') as f:
        json.dump(to_user_data, f, indent=4)

    print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] {from_user_id} gave {quantity} of item {item_name} to {toUserName}.")
    return {"message": 
    f"During proccessing the command, i found out you're the bot owner. Now You won't lose any items from your inventory.\n\n" 
    f"Successfully gave {quantity} of item {item_name} to {toUserName} without affecting your inventory."}
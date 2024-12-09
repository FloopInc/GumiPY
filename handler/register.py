import json,os,time
from telegram import Update
from telegram.ext import ContextTypes
from colorama import Fore, Style
STATUSFILE = 'data/UserStatus.json'
PASSWORD = "OZMoon"
TEXTMAP = 'data/TextMap.json'


def loadOwner():
    with open('data/config.json') as config_file:
        config_data = json.load(config_file)
        return config_data["Owner"]
    
def loadUserStatus():
    if os.path.exists(STATUSFILE):
        with open(STATUSFILE, 'r') as f:
            data = json.load(f)
            if isinstance(data, dict): 
                return data
    return {}

def saveUserStatus(userStatus):
    with open(STATUSFILE, 'w') as f:
        json.dump(userStatus, f, indent=4)

def loadTextMap():
    if os.path.exists(TEXTMAP):
        with open(TEXTMAP, 'r') as f:
            return json.load(f)
    return{}

def getTextMap(key):
    textMap = loadTextMap()
    return textMap.get(key, "")

def loadUserProfile(user_id):
    profile_file = f'user/{user_id}.json'
    if os.path.exists(profile_file):
        with open(profile_file, 'r') as f:
            return json.load(f)
    return {}

def userStats(user_id: int, username: str):
    userStatus = loadUserStatus()
    userStatus[str(user_id)] = {
            "username": username,
            "registered": False,
            "isBanned": False,
            "isModerator": False,
            "isHidden": False,
            "isRadio": True,
            "banExpires": 0
            }
    saveUserStatus(userStatus)
def saveUserProfile(user_id, profile_data):
    profile_file = f'user/{user_id}.json'
    with open(profile_file, 'w') as f:
        json.dump(profile_data, f, indent=4)

def isRegistered(user_id):
    userStatus = loadUserStatus()
    return userStatus.get(str(user_id), {}).get('registered', False)

def isMod(user_id):
    userStatus = loadUserStatus()
    return userStatus.get(str(user_id), {}).get('isModerator', True)

def format_remaining_time(seconds):
    days = seconds // (24 * 3600)
    seconds %= 24 * 3600
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{days}d {hours}h {minutes}m {seconds}s"

def isBanned(user_id):
    userStatus = loadUserStatus()
    userProfile = loadUserProfile(user_id)

    banReason = userProfile.get('banReason', '')
    username = userProfile.get('username', '')
    user_data = userStatus.get(str(user_id), {})
    if not user_data.get('isBanned', False):
        return None
    
    ban_expires = user_data.get('banExpires', None)
    if ban_expires is None:
        return getTextMap("isBanned")
    
    current_time = int(time.time())
    if current_time < ban_expires:
        remaining_time = ban_expires - current_time
        remaining_time_str = format_remaining_time(remaining_time)
        return f"🚫 Sorry, but Your Account has been temporarily suspended.\nBan Reason: `{banReason}`\nThis temporary ban will be removed in **{remaining_time_str}**. If you didn't do anything wrong & believe this is a mistake please contact /mods"
    else:
        user_data['isBanned'] = False
        userStatus[str(user_id)] = user_data
        saveUserStatus(userStatus)
        return None 

def unregister(user_id):
    userStatus = loadUserStatus()
    if str(user_id) in userStatus:
        userStatus[str(user_id)]['registered'] = False
        saveUserStatus(userStatus)
        return {"message": getTextMap("unregisterSuccess")}
    return {"message": getTextMap("notFound")}

def register(user_id, password):
    userStatus = loadUserStatus()
    username = userStatus.get(str(user_id), {}).get('username', '')
    if password != PASSWORD:
        print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{Fore.RED}ERROR{Style.RESET_ALL}] User {user_id}/{username} Input Invalid Password during register account: {password}")
        return {"message": getTextMap("invalidPassword")}


    if not isinstance(userStatus, dict):
        return {"message": getTextMap("internalError")}

    userStatus[str(user_id)]['registered'] = True
    saveUserStatus(userStatus)

    print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{Fore.BLUE}INFO{Style.RESET_ALL}] User {user_id}/{username} registered account.")
    return {"message": getTextMap("registerSuccess")}


def ban(user_id, reason="", duration=0):
    userStatus = loadUserStatus()

    if str(user_id) in userStatus:
        userStatus[str(user_id)]['isBanned'] = True
        userStatus[str(user_id)]['registered'] = False
        userStatus[str(user_id)]['isRadio'] = False
        userStatus[str(user_id)]['isModerator'] = False

        if duration > 0:
            userStatus[str(user_id)]['banExpires'] = int(time.time()) + duration
        else:
            userStatus[str(user_id)]['banExpires'] = None 

        saveUserStatus(userStatus)

        userProfile = loadUserProfile(user_id)
        if "logs" not in userProfile:
            userProfile["logs"] = []

        if reason:
            userProfile["banReason"] = reason
            userProfile["logs"].append({"action": "ban", "reason": reason})

        saveUserProfile(user_id, userProfile)

        return {"message": getTextMap("banned")}

    return {"message": getTextMap("notFound")}


def unban(user_id, reason=""):
    userStatus = loadUserStatus()
    
    if str(user_id) in userStatus:
        userStatus[str(user_id)]['isBanned'] = False
        userStatus[str(user_id)]['banExpires'] = None
        saveUserStatus(userStatus)
        
        userProfile = loadUserProfile(user_id)
        if "logs" not in userProfile:
            userProfile["logs"] = []
        
        if reason:
            userProfile["logs"].append({"action": "unban", "reason": reason})

        saveUserProfile(user_id, userProfile)
        
        return {"message": getTextMap("unbanned")}
    
    return {"message": getTextMap("notFound")}

async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message_text = update.message.text.strip()
    password = message_text.split(" ")[1] if len(message_text.split(" ")) > 1 else None

    if isBanned(user_id):
        await update.message.reply_text(isBanned(user_id), parse_mode='Markdown')
        return
    
    if isRegistered(user_id):
        await update.message.reply_text(getTextMap("registered"))
        return
    
    registration_response = register(user_id, password)
    await update.message.reply_text(registration_response["message"])
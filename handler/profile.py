import json
import os
from handler.register import loadUserStatus, loadOwner, loadUserProfile, saveUserProfile

STATUSFILE = 'data/UserStatus.json'
# Path to redeem folder
REDEEM_FOLDER = 'user/redeem/'

def saveRedeemCode(code: str, redeem_data: dict):
    code = code.lower()
    filepath = f"{REDEEM_FOLDER}{code}.json"
    os.makedirs(REDEEM_FOLDER, exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(redeem_data, f, indent=4)

def loadRedeemCode(code: str):
    code = code.lower()
    filepath = f"{REDEEM_FOLDER}{code}.json"
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return None

def deleteRedeemCode(code: str):
    code = code.lower()
    filepath = f"{REDEEM_FOLDER}{code}.json"
    if os.path.exists(filepath):
        os.remove(filepath)

def getUserIdFromUsername(username):
    userStatus = loadUserStatus()
    for user_id, status in userStatus.items():
        if status.get("username", "").lower() == username.lower():
            return user_id
    return None
def getUsernameFromUserId(user_id):
    userProfile = loadUserProfile(user_id)
    return userProfile.get('name', 'user')

def inspectProfile(user_id):
    userStatus = loadUserStatus()
    userProfile = loadUserProfile(user_id)
    ownerID = loadOwner()
    profileInfo = {}

    status_messages = {
        "registered": "Account Registered"
    }

    if user_id == ownerID:
        profileInfo = {key: userProfile[key] for key in ['name', '1000', '1001', '1002', '1003', '1005', '1007', '1008', '1010', '1011', '1012', '1013', '1014', '1015'] if key in userProfile}
    elif str(user_id) in userStatus:
        for key, value in userStatus[str(user_id)].items():
            if key in status_messages:
                profileInfo[status_messages[key]] = 'Yes' if value else 'No'
        
        profileInfo.update({key: userProfile[key] for key in ['name', '1000', '1001', '1002', '1003', '1005', '1007', '1008', '1010', '1011', '1012', '1013', '1014', '1015'] if key in userProfile})

    return profileInfo, userProfile.get('name', 'user')

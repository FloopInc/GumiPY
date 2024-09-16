import json
from handler.register import getTextMap
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

def getEventMessage():
    events = loadEventData()
    event_messages = []

    if events.get("CrownDay"):
        event_messages.append(getTextMap("CrownDay"))

    if events.get("BroadcastDay"):
        event_messages.append(getTextMap("BroadcastDay"))

    return "\n\n".join(event_messages) if event_messages else None
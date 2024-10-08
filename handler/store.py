import os,json,random,time,colorama
from handler.economy import loadItems
from handler.register import getTextMap

def getStoreItems():
    items = loadItems()
    store_items = []

    for item_id, item_data in items.items():
        if item_data.get("untradeable"):
            continue  # Skip untradeable items

        if item_data["stock"] == 0:
            out_of_order_messages = [
                "Out of stock!",
                "Currently unavailable!",
                "Out of order!",
                "Check back later!"
            ]
            stock_message = random.choice(out_of_order_messages)
        else:
            stock_message = f"Stock: {item_data['stock']}"

        store_items.append({
            "id": item_id,
            "name": item_data["name"],
            "logo": item_data["logo"],
            "buy": item_data["buy"],
            "sell": item_data["sell"],
            "stock_message": stock_message
        })

    return store_items

def buyItem(user_id: int, item_name: str, quantity: int):
    items = loadItems()
    user_filepath = f'user/{user_id}.json'
    
    if not os.path.exists(user_filepath):
        return {"message": "User data not found."}

    with open(user_filepath, 'r') as f:
        user_data = json.load(f)
    
    item_id = None
    for key, value in items.items():
        if value["name"].lower() == item_name.lower():
            item_id = key
            break

    if not item_id or item_id not in items:
        return {"message": f"Item '{item_name}' not found in store."}
    
    item_data = items[item_id]

    if item_data.get("untradeable"):
        return {"message": getTextMap("untradeable")}
    
    if item_data["stock"] == 0:
        return {"message": random.choice([
            "Out of stock!",
            "Currently unavailable!",
            "Out of order!"
        ])}

    total_cost = item_data["buy"] * quantity

    if user_data["1000"] < total_cost:
        return {"message": getTextMap("notEnoughMoney")}

    user_data["1000"] -= total_cost

    items[item_id]["stock"] -= quantity
    if items[item_id]["stock"] < 0:
        items[item_id]["stock"] = 0

    user_data.setdefault(item_id, 0)
    user_data[item_id] += quantity

    with open(user_filepath, 'w') as f:
        json.dump(user_data, f, indent=4)

    with open('data/items.json', 'w') as f:
        json.dump(items, f, indent=4)
    
    print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] User {user_id} bought {quantity} x {item_data['name']} for {total_cost} 💵 Money!")
    return {"message": f"Successfully purchased {quantity} x {item_data['logo']} {item_data['name']} for {total_cost} 💵 Money!"}

def sellItem(user_id: int, item_name: str, quantity: int):
    items = loadItems()
    user_filepath = f'user/{user_id}.json'
    
    if not os.path.exists(user_filepath):
        return {"message": "User data not found."}

    with open(user_filepath, 'r') as f:
        user_data = json.load(f)
    
    item_id = None
    for key, value in items.items():
        if value["name"].lower() == item_name.lower():
            item_id = key
            break

    if not item_id or item_id not in items:
        return {"message": f"Item '{item_name}' not found in inventory."}
    
    item_data = items[item_id]

    if item_data.get("untradeable"):
        return {"message": getTextMap("untradeable")}

    if user_data.get(item_id, 0) < quantity:
        return {"message": "You don't have that item to sell"}

    total_sell_price = item_data["sell"] * quantity

    user_data[item_id] -= quantity
    if user_data[item_id] < 0:
        user_data[item_id] = 0

    user_data["1000"] += total_sell_price

    items[item_id]["stock"] += quantity
    
    with open(user_filepath, 'w') as f:
        json.dump(user_data, f, indent=4)

    with open('data/items.json', 'w') as f:
        json.dump(items, f, indent=4)
    
    print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{colorama.Fore.BLUE}INFO{colorama.Style.RESET_ALL}] User {user_id} sold {quantity} x {item_data['name']} for {total_sell_price} 💵 Money!")
    return {"message": f"Successfully sold {quantity} x {item_data['logo']} {item_data['name']} for {total_sell_price} 💵 Money!"}

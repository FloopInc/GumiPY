from main import *
import random, requests
def searchJson(keyword, data, limit=10):
    matches = []
    unique_messages = set()  

    for key, value in data.items():
        message = str(value)
        if keyword.lower() in message.lower() and message not in unique_messages:
            unique_messages.add(message) 
            matches.append(f'{value}')

    if len(matches) > limit:
        matches = random.sample(matches, limit)

    return matches, len(unique_messages)  

def linkLargeJson(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"[{int(time.time()) % 86400 // 3600:02d}:{(int(time.time()) % 3600) // 60:02d}:{time.time() % 60:02.0f}] [{Fore.RED}ERROR{Style.RESET_ALL}] Error fetching JSON From GitHub: {e}")
    
async def search_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    args = context.args

    if isBanned(user_id):
        await update.message.reply_text(isBanned(user_id), parse_mode="Markdown")
        return
    if not isRegistered(user_id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return
    if len(args) < 2:
        await update.message.reply_text("Please provide a keyword/action to search.")
        return
    
    action = args[0].lower()
    keyword = " ".join(args[1:])

    if action in ["txtmapdiff", "hsrbetadiff", "latestbetadiff" "textmapendiff", "txtmapdiff"]:
        urls = f'https://raw.githubusercontent.com/PutraZC/HSR_Data/refs/heads/main/TextMapDiff.json'
    elif action in ["textmapen", "txtmapfull", "latestbeta", "textmapfull", "txtmapen"]:
        urls = f'https://raw.githubusercontent.com/PutraZC/HSR_Data/refs/heads/main/TextMapEN.json'
    else:
        await update.message.reply_text("Invalid action. Please provide a valid action.")
        return
    
    json_data = linkLargeJson(urls) 

    if json_data:  
        results, total_found = searchJson(keyword, json_data)  

        if results:
            response_message = f"HSR (2.6.52) Found {total_found} unique result(s) for '{keyword}':\n\n" + "\n\n".join(results)
            await update.message.reply_text(response_message) 
        else:
            await update.message.reply_text(f"No results found for '{keyword}'.")
    else:
        await update.message.reply_text("Failed to fetch the data from the source.")
import tempfile,requests,json,os,time
from telegram import Update
from telegram.ext import ContextTypes

def download_file(url):
    response = requests.get(url)
    response.raise_for_status() 
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
    with open(temp_file.name, 'wb') as f:
        f.write(response.content)
    return temp_file.name

def compare_json_files(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r', encoding='utf-8-sig') as f2:
        json1 = json.load(f1)
        json2 = json.load(f2)
    # diff = {key: json1[key] for key in json1 if key not in json2 or json1[key] != json2[key]}
    # return diff
    new_entries = {key: json2[key] for key in json2 if key not in json1 and json2[key] != "..."}
    return new_entries

async def textmapdiff_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = context.user_data
    
    if 'file1' not in user_data:
        await update.message.reply_text("Please send the link to the first JSON file.")
        user_data['awaiting_file'] = 'file1'
        return
    
    elif 'file2' not in user_data:
        await update.message.reply_text("Please send the link to the second JSON file.")
        user_data['awaiting_file'] = 'file2'
        return

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    user_data = context.user_data

    if 'awaiting_file' in user_data:
        file_key = user_data['awaiting_file']
        try:
            downloaded_file = download_file(message)
            user_data[file_key] = downloaded_file
            del user_data['awaiting_file']

            await update.message.reply_text(f"Downloading File Please Wait...")

            if file_key == 'file1':
                await update.message.reply_text("Please send the link to the second JSON file.")
                user_data['awaiting_file'] = 'file2'
                return

            elif file_key == 'file2':
                if 'file1' in user_data and 'file2' in user_data:
                    file1 = user_data['file1']
                    file2 = user_data['file2']
                    diff = compare_json_files(file1, file2)

                    if diff:
                        result_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
                        with open(result_file.name, 'w', encoding='utf-8') as f:
                            json.dump(diff, f, indent=4)

                        await update.message.reply_document(document=open(result_file.name, 'rb', encoding='utf-8'), filename="TextMapDiff.json")
                        os.remove(result_file.name)
                    else:
                        await update.message.reply_text("No differences found between the two JSON files.")
                    
                    os.remove(file1)
                    os.remove(file2)
                    del user_data['file1']
                    del user_data['file2']
        except Exception as e:
            await update.message.reply_text(f"Failed to download the file: {e}")
            return
import requests
import base64
import json
import re
from telegram import Update
from telegram.ext import ContextTypes
from handler.register import isRegistered, isBanned, getTextMap

with open('data/dispatch.json') as config_file:
    config_data = json.load(config_file)

async def check_version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args

    if isBanned(update.message.from_user.id):
        await update.message.reply_text(isBanned(update.message.from_user.id), parse_mode='Markdown')
        return
    
    if not isRegistered(update.message.from_user.id):
        await update.message.reply_text(getTextMap("notRegistered"))
        return

    if len(args) < 2:
        await update.message.reply_text(getTextMap("provideVersion"))
        return

    action = args[0].lower()
    version = args[1]

    if action in ["osstarrailbeta", "ossrbeta"]:
        encoded_url = config_data["os_sr_beta"]
    elif action in ["cnstarrailbeta", "cnsrbeta"]:
        encoded_url = config_data["cn_sr_beta"]
    elif action in ["osstarrailprod", "ossrprod"]:
        encoded_url = config_data["os_sr_prod"]
    elif action in ["cnstarrailprod", "cnsrprod"]:
        encoded_url = config_data["cn_sr_prod"]
    elif action in ["osce", "ossrce", "oscecreation"]:
        encoded_url = config_data["os_sr_ce"]
    elif action in ["cnce", "cnsrce", "cncecreation"]:
        encoded_url = config_data["cn_sr_ce"]
    else:
        await update.message.reply_text(getTextMap("invalidCheck"))
        return

    deurl = base64.b64decode(encoded_url).decode('utf-8')
    url = f'{deurl}{version}&language_type=3&platform_type=1&channel_id=1&sub_channel_id=1&is_new_format=1'
    
    try:
        response = requests.get(url)
        response.raise_for_status()

        decoded_data = base64.b64decode(response.content)
        message = decode_protobuf_message(decoded_data).get('msg', 'No Message Found')

        response_message = (
            f"Response Status Code: {response.status_code}\n\n"
            f"Raw Message Content for Version {version}: {decoded_data}\n\n"
            f"Result Message: {message}\n\n"
        )

        urls = extract_urls(str(decoded_data))
        if urls:
            urls_message = "URLs:\n" + "\n".join(urls)
        else:
            urls_message = "URLs: No URLs found."
        
        response_message += urls_message
        
        await update.message.reply_text(response_message)

    except requests.exceptions.RequestException as e:
        print(f'Error making request: {e}')
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def decode_protobuf_message(data):
    message = {}
    offset = 0
    while offset < len(data):
        field_header = data[offset]
        field_number = field_header >> 3
        wire_type = field_header & 0b111
        offset += 1
        
        if wire_type == 0:
            varint = 0
            shift = 0
            while True:
                byte = data[offset]
                varint |= (byte & 0b01111111) << shift
                offset += 1
                if byte < 0b10000000:
                    break
                shift += 7
            if field_number == 1:
                message['retcode'] = varint

        elif wire_type == 2:
            length = data[offset]
            offset += 1
            value = data[offset:offset + length]
            offset += length
            decoded_value = value.decode('utf-8', errors='ignore')  # Decode safely
            
            filtered_value = re.sub(r'[^\w\s,.!?]', '', decoded_value)
            
            if field_number == 2 or "msg" not in message:
                message['msg'] = filtered_value
            elif field_number == 3:
                message['top_sever_region_name'] = filtered_value
            elif field_number == 5:
                message['stop_desc'] = filtered_value
            else:
                message[f'field_{field_number}'] = filtered_value

        elif wire_type == 2:
            repeated_length = data[offset]
            offset += 1
            repeated_value = data[offset:offset + repeated_length]
            offset += repeated_length
            if 'regionList' not in message:
                message['regionList'] = []
            message['regionList'].append(repeated_value.decode('utf-8', errors='ignore'))
    return message


def extract_urls(text):
    urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    return urls
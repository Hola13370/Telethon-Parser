from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv
import re
from datetime import datetime
import colorama
from colorama import Fore, init

def client_telethon(api_id, api_hash, phone):
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('Telethon input code: '))
    return client

def grouplist(client):
    chats = []
    last_date = None
    chunk_size = 200
    groups = []
    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup:
                groups.append(chat)
        except:
            continue
    return groups

def sanitize_filename(filename):
    sanitized_filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return sanitized_filename

def save_participants(client, target_group):
    try:
        all_participants = client.get_participants(target_group, aggressive=True)
        filename = sanitize_filename(target_group.title)
        with open(f"{filename}.txt", "w", encoding='utf-8') as f:
            f.write("username\tuser id\taccess hash\tname\tgroup\tgroup id\n")
            for user in all_participants:
                username = user.username if user.username else ""
                name = f"{user.first_name} {user.last_name}".strip()
                f.write(f"{username}\t{user.id}\t{user.access_hash}\t{name}\t{target_group.title}\t{target_group.id}\n")
        print(Fore.RED + f"{datetime.now()} User participants exported to {filename}.txt")
    except Exception as e:
        print(Fore.RED + f"Error occurred: {e}")
from colorama import Fore
from colorama import init
from session import client_telethon, grouplist, save_participants

init(autoreset=True)

def main():
    api_id, api_hash, phone = get_api_credentials()
    client = client_telethon(api_id, api_hash, phone)
    groups = grouplist(client)
    print(Fore.GREEN + 'groups.user.append:')
    for i, g in enumerate(groups):
        print(Fore.GREEN + str(i) + '=>' + g.title)
        save_participants(client, g)
    print(Fore.GREEN + "Done")

def get_api_credentials():
    from config import api_id, api_hash, phone
    return api_id, api_hash, phone

if __name__ == "__main__":
    main()
import requests
from core import TOKEN, BASE_API

headers = {
    "Authorization": TOKEN,
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9235 Chrome/138.0.7204.251 Electron/37.6.0 Safari/537.36"
}

def get_dms():
    return requests.get(
        f"{BASE_API}/users/@me/channels",
        headers=headers
    ).json()


def get_friends():
    return requests.get(
        f"{BASE_API}/users/@me/relationships",
        headers=headers
    ).json()

def send_message(channel_id, content):
    return requests.post(
        f"{BASE_API}/channels/{channel_id}/messages",
        headers=headers,
        json={"content": content}
    )
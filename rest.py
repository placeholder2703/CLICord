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

def get_info(user_id=None):
	if not user_id:
		user_id = "@me"
	return requests.get(
		f"{BASE_API}/users/{user_id}",
		headers=headers
	).json()

def get_guilds(guild_id=None):
	if guild_id is not None:
		return requests.get(
			f"{BASE_API}/guilds/{guild_id.strip()}",
			headers=headers
		).json()
	else:
		return requests.get(
			f"{BASE_API}/users/@me/guilds",
			headers=headers
		).json()

def get_channel(channel_id):
	return requests.get(
		f"{BASE_API}/channels/{channel_id}",
		headers=headers
		).json()

def send_message(channel_id, content):
	return requests.post(
		f"{BASE_API}/channels/{channel_id}/messages",
		headers=headers,
		json={"content": content}
	)
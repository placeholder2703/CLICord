import requests
import asyncio
from core import BASE_API
import core

def _headers():
	return {
		"Authorization": core.TOKEN,
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9235 Chrome/138.0.7204.251 Electron/37.6.0 Safari/537.36"
	}

async def get_dms():
	return await asyncio.to_thread(
		lambda: requests.get(
			f"{BASE_API}/users/@me/channels",
			headers=_headers()
		).json()
	)


async def get_friends():
	return await asyncio.to_thread(
		lambda: requests.get(
			f"{BASE_API}/users/@me/relationships",
			headers=_headers()
		).json()
	)


async def get_info(user_id=None):
	if not user_id:
		user_id = "@me"

	return await asyncio.to_thread(
		lambda: requests.get(
			f"{BASE_API}/users/{user_id}",
			headers=_headers()
		).json()
	)


async def get_guilds(guild_id=None):
	return await asyncio.to_thread(
		lambda: requests.get(
			f"{BASE_API}/guilds/{guild_id.strip()}" if guild_id else f"{BASE_API}/users/@me/guilds",
			headers=_headers()
		).json()
	)


async def get_channel(channel_id):
	return await asyncio.to_thread(
		lambda: requests.get(
			f"{BASE_API}/channels/{channel_id}",
			headers=_headers()
		).json()
	)


async def get_message(channel_id, depth=10):
	return await asyncio.to_thread(
		lambda: requests.get(
			f"{BASE_API}/channels/{channel_id}/messages?limit={depth}",
			headers=_headers()
		).json()
	)
	
async def send_message(channel_id, content):
	return await asyncio.to_thread(
		lambda: requests.post(
			f"{BASE_API}/channels/{channel_id}/messages",
			headers=_headers(),
			json={"content": content}
		)
	)


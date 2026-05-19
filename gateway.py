from core import state, TOKEN, GATEWAY_URL
import websockets
import json
import asyncio
import random

ws = None
heartbeat_task = None

heartbeat_interval = 0
sequence = None
session_id = None
resume_url = None
should_resume = False
last_ack = True
missed_ack = 0

async def send_ws(data):
	global ws
	if ws is None:
		return
	await ws.send(json.dumps(data))

async def set_status(status, activities=None):
	global ws
	await send_ws({
		"op": 3,
		"d": {
			"since": None,
			"activities": activities if activities else [],
			"status": status,
			"afk": status == "idle"
		}
	})

async def heartbeat_loop():
	global ws, last_ack, missed_ack
	interval = heartbeat_interval / 1000
	while True:
		if not last_ack:
			missed_ack += 1
			if missed_ack >= 3:
				print(f"Server failed to acknowledge {missed_ack} heartbeats, reconnecting")
				await ws.close()
				return
		last_ack = False
		await send_ws({
			"op": 1,
			"d": sequence
		})
		await asyncio.sleep(interval)

async def identify():
	await send_ws({
		"op": 2,
		"d": {
			"token": TOKEN,
			"capabilities": 30717,
			"compress": False,
			"properties": {
				"os": "Windows",
				"browser": "Chrome",
				"device": "",
				"system_locale": "en-US",
				"browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
				"browser_version": "136.0.0.0",
				"os_version": "10",
				"referrer": "",
				"referring_domain": "",
				"release_channel": "stable",
				"client_build_number": 9999,
				"client_event_source": None
			},
			"presence": {
				"status": "online",
				"since": 0,
				"activities": [],
				"afk": False
			}
		}
	})

async def resume():
	global ws
	print("Attempting resumption")
	await send_ws({
		"op": 6,
		"d": {
			"token": TOKEN,
			"session_id": session_id,
			"seq": sequence
		}
	})

async def handle_packet(packet):
	global ws, heartbeat_task, heartbeat_interval, last_ack, missed_ack
	global sequence, session_id, resume_url, should_resume
	if packet.get("s") is not None:
		sequence = packet["s"]
	op = packet.get("op")
	data = packet.get("d")
	event = packet.get("t")

	if op == 0:
		if event == "MESSAGE_CREATE":
			if data["channel_id"] == state["selected_channel"]:
				print(f"{data["author"]["global_name"]} ({data["author"]["username"]}): {data["content"]}")

	if op == 1:
		await send_ws({
			"op": 1,
			"d": sequence
		})

	if op == 7:
		print("Server requested reconnection")
		should_resume = True
		await ws.close()

	if op == 9:
		await asyncio.sleep(random.uniform(1, 5))
		if data:
			print("Opcode 9 but d: True, resuming")
			should_resume = True
		else:
			print("Session invalidated, reauthenticating")
			should_resume = False
			sequence = None
			session_id = None
		await ws.close()

	if op == 10:
		heartbeat_interval = data["heartbeat_interval"]
		last_ack = True
		missed_ack = 0
		if heartbeat_task:
			heartbeat_task.cancel()
		heartbeat_task = asyncio.create_task(heartbeat_loop())
		if (should_resume and session_id and sequence is not None):
			await resume()
		else:
			await identify()
		
	if op == 11:
		last_ack = True
		missed_ack = 0

	if event == "READY":
		print("Logged in as", data["user"]["username"])
		resume_url = data["resume_gateway_url"]
		session_id = data["session_id"]
		should_resume = False

	if event == "RESUMED":
		print("Successfully resumed")

async def gateway_loop():
	global ws, should_resume, session_id, sequence
	ws_url = GATEWAY_URL
	while True:
		try:
			async with websockets.connect(ws_url, ping_interval=None) as websocket:
				ws = websocket
				print("Gateway connected")
				async for message in ws:
					packet = json.loads(message)
					await handle_packet(packet)
		except websockets.ConnectionClosed as e: # Always closing with 1006 for some reason
			print("Gateway closed", e.code, e.reason)
			if e.code in (
				4003, # Not authenticated
				4004, # Authentication failed
				4005, # Already authenticated
				4006, # Session no longer valid
				4007, # Invalid seq
				4009, # Session timed out
				4010, # Invalid shard
				4011, # Sharding required
				4012, # Invalid API version
				4013, # Invalid intents
				4014, # Disallowed intents
				4015, # Too many sessions
				4016  # Connection request canceled
			):
				print("Session invalidated, re-identifying")
				session_id = None
				sequence = None
				should_resume = False
			else:
				print("Disconnected, resuming")
				should_resume = True
		except Exception as e:
			print("Gateway error:", e)
		finally:
			if heartbeat_task:
				heartbeat_task.cancel()	
		if should_resume and resume_url:
			ws_url = ( f"{resume_url}" f"/?v=9&encoding=json" )
		else:
			ws_url = GATEWAY_URL

		await asyncio.sleep(2 + random.random())
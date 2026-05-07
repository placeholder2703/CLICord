from core import state, TOKEN, GATEWAY_URL
from websocket import WebSocketApp
import json
import threading
import time
import random

stop_event = threading.Event()
hb_thread = None

heartbeat_interval = 0
sequence = None
session_id = None
resume_url = None
should_resume = False
last_ack = True
missed_ack = 0

def send_ws(ws, data):
	if ws is None or stop_event.is_set():
		return
	try:
		ws.send(json.dumps(data))
	except Exception as e:
		print("Send failed:", e)

def set_status(status, activities=None):
	send_ws(ws, {
		"op": 3,
		"d": {
			"since": None,
			"activities": activities if activities else [],
			"status": status,
			"afk": status == "idle"
		}
	})

def heartbeat_loop(local_ws):
	global last_ack, missed_ack
	interval = heartbeat_interval / 1000
	while not stop_event.wait(interval):
		if not last_ack:
			missed_ack += 1
			if missed_ack >= 3:
				print(f"Server failed to acknowledge {missed_ack} heartbeats, reconnecting")
				local_ws.close()
				return
		last_ack = False
		send_ws(local_ws, {
			"op": 1,
			"d": sequence
		})

def identify(ws):
	send_ws(ws, {
		"op": 2,
		"d": {
			"token": TOKEN,
			"properties": {
				"os": "windows",
				"browser": "websocket-client",
				"device": "python"
			}
		}
	})

def on_open(ws):
	print("Gateway connected")

def resume(ws):
	print("Attempting resumption")
	send_ws(ws, {
		"op": 6,
		"d": {
			"token": TOKEN,
			"session_id": session_id,
			"seq": sequence
		}
	})

def on_message(ws, message):
	global heartbeat_interval, sequence, hb_thread, session_id, resume_url, should_resume, last_ack, missed_ack
	packet = json.loads(message)
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
		send_ws(ws, {
			"op": 1,
			"d": sequence
		})

	if op == 7:
		print("Server requested reconnection")
		stop_event.set()
		should_resume = True
		ws.close()

	if op == 9:
		stop_event.set()
		if data:
			print("Opcode 9 but d: True, resuming")
			should_resume = True
		else:
			print("Session invalidated, reauthenticating")
			should_resume = False
			sequence = None
			session_id = None
		ws.close()

	if op == 10:
		heartbeat_interval = data["heartbeat_interval"]
		last_ack = True
		if hb_thread is not None:
			stop_event.set()
			time.sleep(0.5)
			stop_event.clear()
		hb_thread = threading.Thread(
		target=heartbeat_loop,
			args=(ws,),
			daemon=True
		)
		hb_thread.start()
		if should_resume and session_id and sequence is not None:
			resume(ws)
		else:
			identify(ws)
		
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

def on_close(ws, code, reason):
	global hb_thread, should_resume, session_id, sequence
	print("Gateway close ", code, reason)
	stop_event.set()
	if code in (
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
	
	elif should_resume and code in (
		4000, # Unknown error
		4001, # Unknown opcode
		4002, # Decode error
		4008,  # Rate limited
		None
	):
		print("Disconnected, resuming")
		should_resume = True
	if hb_thread is not None:
		hb_thread.join()
	hb_thread = None

def on_error(ws, error):
	print("Gateway error: ", error)

def start_gateway():
	global ws
	ws_url = GATEWAY_URL
	while True:
		stop_event.clear()
		ws = WebSocketApp(
			ws_url,
			on_open=on_open,
			on_message=on_message,
			on_error=on_error,
			on_close=on_close
		)
		ws.run_forever(ping_interval=0)
		if should_resume and resume_url:
			ws_url = f"{resume_url}/?v=9&encoding=json"
		else:
			ws_url = GATEWAY_URL
		time.sleep(2 + random.random())

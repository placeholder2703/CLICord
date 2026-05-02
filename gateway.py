from core import state, TOKEN, GATEWAY_URL, send_ws
from websocket import WebSocketApp
import json
import threading
import time

def identify():
	send_ws(ws, {
		"op": 2,
		"d": {
			"token": TOKEN,
			"properties": {
				"os": "Windows",
				"browser": "CLICord",
				"device": ""
			}
		}
	})

def heartbeat_loop():
	while True:
		time.sleep(heartbeat_interval / 1000)
		send_ws(ws, {
			"op": 1,
			"d": sequence
		})

def set_status(status, text=None):
    activity = None
    if text:
        activity = {
            "type": 4,
            "name": "Custom Status",
            "state": text
        }
    send_ws(ws, {
        "op": 3,
        "d": {
            "since": None,
            "activities": [activity] if activity else [],
            "status": status,
            "afk": status == "idle"
        }
    })

def on_open(socket):
	print("Gateway connected.")


def on_message(socket, message):
	global heartbeat_interval
	global sequence
	packet = json.loads(message)
	if packet.get("s") is not None:
		sequence = packet["s"]
	op = packet.get("op")
	data = packet.get("d")
	event = packet.get("t")
	if op == 10:
		heartbeat_interval = data["heartbeat_interval"]
		threading.Thread(
			target=heartbeat_loop,
			daemon=True
		).start()
		identify()
	if op == 0:
		if event == "MESSAGE_CREATE":
			if data["channel_id"] == state["selected_channel"]:
				print(f"{data["author"]["global_name"]} ({data["author"]["username"]}): {data["content"]}")
	if event == "READY":
		print("Logged in as", data["user"]["username"])
def on_close(socket, code, reason):
	print("Gateway close ", code, reason)

def on_error(socket, error):
	print("Gateway error: ", error)

def start_gateway():
	global ws

	ws = WebSocketApp(
		GATEWAY_URL,
		on_open=on_open,
		on_message=on_message,
		on_close=on_close,
		on_error=on_error
	)

	ws.run_forever()
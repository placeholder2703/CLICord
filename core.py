import json
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
BASE_API = "https://discord.com/api/v10"
GATEWAY_URL = "wss://gateway.discord.gg/?v=9&encoding=json"

state = {
    "sequence": None,
    "session_id": None,
    "heartbeat_interval": None,
    "selected_channel": None
}

def send_ws(ws, data):
    ws.send(json.dumps(data))
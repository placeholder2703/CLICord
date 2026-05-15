TOKEN = None
BASE_API = "https://discord.com/api/v9"
GATEWAY_URL = "wss://gateway.discord.gg/?v=9&encoding=json"

state = {
	"sequence": None,
	"session_id": None,
	"heartbeat_interval": None,
	"selected_channel": None
}


import threading
from gateway import start_gateway
from rest import send_message
from commands import handle
import core
import sys
import json

sys.stdout.reconfigure(encoding="utf-8")
if sys.version_info < (3, 12):
    print("Because of the double quotes in f-strings AND my laziness, CLICord requires Python 3.12+")
    sys.exit(1)

print("This is CLICord(pronounced cli(ng)-cord, C-L-I Cord or whatever), a Python CLI Discord client.")
print("Being a CLI app takes away all of that Electron chrome-based GUI BS")
print("Making this an very lightweight client while still being functional.")

try:
    with open("users.json", "r", encoding="utf8") as f:
        accounts = json.load(f)
except FileNotFoundError:
    print("users.json not found")
    exit()

print("Choose an account:")
keys = list(accounts.keys())

for index, key in enumerate(keys):
    print(f"[{index}] {key}")
core.TOKEN = accounts[keys[int(input("> "))]]

channel_id = None
threading.Thread(
	target=start_gateway,
	daemon=True
).start()

while True:
	text = input()
	if not text.startswith("."):
		if core.state["selected_channel"]:
			send_message(core.state["selected_channel"], text)
		else:
			print("Set channel ID first, get it from .dms and set with .changechannel")
	else:
		out = handle(text)
		if out: print(out)
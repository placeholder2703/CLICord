#changes made: indentation

import core
import sys
import json

sys.stdout.reconfigure(encoding="utf-8")

if sys.version_info < (3, 12):
	print("Because of the nested double quotes in f-strings, CLICord requires Python 3.12+ (PEP 701)")
	print(f"And it appears that you're using {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} to run CLICord, update it")
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

print("Choose an account(Empty means 0th account):")
keys = list(accounts.keys())
for index, key in enumerate(keys):
	print(f"[{index}] {key}")

while True:
	account = input("> ").strip()
	if not account:
		account = 0
		break
	if not account.isdigit():
		print("Value must be an integer or empty")
		continue
	account = int(account)
	if 0 <= account < len(keys):
		break
	print("Invalid account index")

core.TOKEN = accounts[keys[account]]

# Actual startup happens down there

import threading
from gateway import start_gateway
from rest import send_message
from commands import handle


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
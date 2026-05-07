from gateway import set_status
from rest import *
from core import state
from colours import C
import json
def generate_name(recipient):
	if recipient.get("user"):
		name = recipient["user"].get("global_name") or recipient["user"]["username"]
		username = recipient["user"]["username"]
	else:
		name = recipient.get("global_name") or recipient["username"]
		username = recipient["username"]
	disc = f"#{C.GRAY}{recipient['discriminator']}{C.RESET}" if recipient.get("discriminator") not in (None, "0") else ""
	bot_tag = " [SYSTEM]" if recipient.get("system") else " [BOT]" if recipient.get("bot") else ""
	return f"{C.CYAN}{name}{C.RESET}{bot_tag} ({C.GRAY}{username}{C.RESET})"
	
def handle(text):
	parts = text.split(" ", 2)
	cmd = parts[0]
	arg1 = parts[1] if len(parts) > 1 else None
	arg2 = parts[2] if len(parts) > 2 else None
	if cmd == ".status":
		if arg1:
			if arg2 is True:
				with open('data.json', 'r', encoding='utf-8') as f:
					data = json.load(f)
			else:
				data = None
			set_status(arg1, data)
		else:
			return "usage: .status <status> <include_activities?>"

	elif cmd == ".friends":
		friends = get_friends()
		for friend in friends:
			print(f"{C.BLUE}{friend['id']}{C.RESET} {generate_name(friend)}")

	elif cmd == ".dms":
		dms = get_dms()
		for dm in dms:
			recipients = dm["recipients"]
			if not recipients:
				continue
			if len(recipients) > 1:
				print(f"{C.BLUE}{dm["id"]}{C.RESET} ({len(recipients) + 1} people including YOU)")
				for recipient in recipients:
					print(f"    {generate_name(recipient)}")
				print(f"    and {C.BOLD}YOU{C.RESET}")
			else:
				recipient = recipients[0]
				print(f"{C.BLUE}{dm["id"]}{C.RESET} {generate_name(recipient)}")

	elif cmd == ".changechannel":
		if arg1 and arg1.strip():
			channel = get_channel(arg1)
			if channel["type"] == 0:
				print(f"You're now chatting in #{channel["name"]}")
			elif channel["type"] == 1:
				print(f"You're now chatting with {generate_name(channel["recipients"][0])}")
			elif channel["type"] == 3:
				print(f"You're now chatting in Group DM {arg1}")
			else:
				return "Unsupported channel type"
			state["selected_channel"] = arg1
		else:
			return "usage: .changechannel <id>"

	# elif cmd == ".guilds":
	# 	if arg:
	# 		guilds = get_guilds(arg)
	# 	else:
	# 		guilds = get_guilds()
	# 	print(guilds)
	
	elif cmd == ".info":
		info = get_info()
		print(f"{C.BLUE}{info["id"]}{C.RESET} {generate_name(info)}")

	elif cmd == ".send":
		if not state["selected_channel"]:
			return "Set channel ID first, get it from .dms and set with .changechannel"
		if arg1:
			send_message(state["selected_channel"], arg1)
		else:
			return "usage: .send <msg>"

	elif cmd == ".help":
		print("""
.status <status> <act?> - Changes your status, if <act?> is True, loads activities from activities.json
.friends                - Fetches friend list
.dms                    - Fetches DMs list
.changechannel <id>     - Changes channel
.list                   - Lists people in Group DM
.info                   - Fetches your info(only ID, username and display name)
.send <msg>             - Sends a message to selected channel(select with .changechannel)
.help                   - Prints this thing
		""")
	else:
		return "Command not found, try using .help, or are you trying to send a message that starts with a dot? send it using .send instead"
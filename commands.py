from gateway import set_status
from rest import *
from core import state
from colours import C
def generate_name(recipient):
	if recipient.get("user"):
		name = recipient["user"].get("global_name") or recipient["user"]["username"]
		username = recipient["user"]["username"]
	else:
		name = recipient.get("global_name") or recipient["username"]
		username = recipient["username"]
	disc = f"#{C.GRAY}{recipient['discriminator']}{C.RESET}" if recipient.get("discriminator") not in (None, "0") else ""
	bot_tag = " [SYSTEM]" if recipient.get("system") else " [BOT]" if recipient.get("bot") else ""
	return f"{C.CYAN}{name}{C.RESET} ({C.GRAY}{username}{C.RESET})"
def handle(text):
	parts = text.split(" ", 1)
	cmd = parts[0]
	arg = parts[1] if len(parts) > 1 else None
	if cmd == ".status":
		if arg:
			set_status(arg)
		else:
			return "usage: .status <status>"

	elif cmd == ".friends":
		friends = get_friends()
		print(friends)
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
		if arg and arg.strip():
			channel = get_channel(arg)
			if channel["type"] == 1:
				print(f"You're now chatting with {generate_name(channel["recipients"][0])}")
			state["selected_channel"] = arg
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
		print(info)

	elif cmd == ".send":
		if not state["selected_channel"]:
			return "Set channel ID first, get it from .dms and set with .changechannel"
		if arg:
			send_message(state["selected_channel"], arg)
		else:
			return "usage: .send <msg>"
	else:
		return "Command not found, are you trying to send a message that starts with a dot? send it using .send instead"
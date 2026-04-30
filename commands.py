from gateway import set_status
from rest import get_dms, get_friends, send_message
from core import state
from colours import C
def handle(text):
	if text.startswith(".status"):
		status = text.split(" ", 1)[1]
		set_status(status)
	if text.startswith(".friends"):
		friends=get_friends()
		for friend in friends:
			user = friend["user"]
			display = user.get("global_name") or user["username"]
			print(f"{C.BLUE}{user['id']}{C.RESET} {C.CYAN}{display}{C.RESET} ({C.GRAY}{user['username']}{C.RESET}) ")
	if text.startswith(".dms"):
		dms=get_dms()
		for dm in dms:
			recipients = dm["recipients"]
			if len(recipients) > 1:
				print(f"{C.BLUE}{dm["id"]}{C.RESET} ({len(recipients) + 1} people including YOU)")
				for recipient in recipients:
					name = recipient.get("global_name") or recipient["username"]
					print(f"    {C.CYAN}{name}{C.RESET} ({C.GRAY}{recipient["username"]}{C.RESET})")
				print(f"    and {C.BOLD}YOU{C.RESET}")
			else:
				recipient = recipients[0]
				name = recipient.get("global_name") or recipient["username"]
				disc = f"#{C.GRAY}{recipient['discriminator']}{C.RESET}" if recipient.get("discriminator") not in (None, "0") else ""
				is_bot = recipient.get("bot")
				print(f"{C.BLUE}{dm["id"]}{C.RESET} {C.CYAN}{name}{C.RESET} ({C.GRAY}{recipient["username"]}{disc}{C.RESET})")
	if text.startswith(".changechannel"):
		channel_id = text.split(" ", 1)[1]
		state["selected_channel"] = channel_id
		return "Selected channel" + channel_id
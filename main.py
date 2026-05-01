import threading
from gateway import start_gateway
from rest import send_message
from commands import handle
from core import state
import sys
sys.stdout.reconfigure(encoding="utf-8")

print("This is CLICord(pronounced cli(ng)-cord, C-L-I Cord or whatever), a Python CLI Discord client")
print("which takes away all of that Electron\n- RAM-consuming\n- CPU-throttling\n- GPU-overloading\n- Battery-draining\n- Memory-leaking\n- PROCESS-SPAWNING\n- THREAD-BLOCKING\n- EVENT-LOOP-FREEZING\n- DISK-SATURATING\n- RESOURCE-HOARDING\nGUI BULLSHIT, ESSPECIALLY ON WEAK DEVICES LIKE MINE.")
print("Making this an very lightweight client while still being functional.")

channel_id = None
threading.Thread(
    target=start_gateway,
    daemon=True
).start()

while True:
    text = input()
    if not text.startswith("."):
        if state["selected_channel"]:
            send_message(state["selected_channel"], text)
        else:
            print("Set channel ID first, get it from .dms and set with .changechannel")
    else:
        out = handle(text)
        if out: print(out)
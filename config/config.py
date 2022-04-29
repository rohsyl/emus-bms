import os
from dotenv import load_dotenv
load_dotenv()

EMUS_SERIAL_PORT = os.getenv("EMUS_SERIAL_PORT")

EMUS_SERIAL_VID = os.getenv("EMUS_SERIAL_VID")
EMUS_SERIAL_PID = os.getenv("EMUS_SERIAL_PID")

NO_BT3 = os.getenv("NO_BT3", False)

EMUS_LIVE_INTERVAL = int(os.getenv("EMUS_LIVE_INTERVAL", 5))
EMUS_LIVE_TIMEOUT = int(os.getenv("EMUS_LIVE_TIMEOUT", 2))
import os
from dotenv import load_dotenv
load_dotenv()

STUDER_SERIAL_PORT = os.getenv("STUDER_SERIAL_PORT")
EMUS_SERIAL_PORT = os.getenv("EMUS_SERIAL_PORT")


WS_LISTEN_PORT = os.getenv("WS_LISTEN_PORT")
WS_SECURE = os.getenv("WS_SECURE")
WS_CERT_PEM = os.getenv("WS_CERT_PEM")

NO_BT3 = os.getenv("NO_BT3", False)
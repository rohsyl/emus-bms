import os
from dotenv import load_dotenv
load_dotenv()

# config
ID = os.getenv("ID")

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

DB_LOCAL_PASS = os.getenv("DB_LOCAL_PASS")
DB_LOCAL_HOST = os.getenv("DB_LOCAL_HOST")
DB_LOCAL_NAME = os.getenv("DB_LOCAL_NAME")
DB_LOCAL_USER = os.getenv("DB_LOCAL_USER")

DB_SYNC_HOST = os.getenv("DB_SYNC_HOST")
DB_SYNC_NAME = os.getenv("DB_SYNC_NAME")
DB_SYNC_USER = os.getenv("DB_SYNC_USER")
DB_SYNC_PASS = os.getenv("DB_SYNC_PASS")

# constants
OPT_DATA = 'data'
OPT_CONST = 'const'

START_BYTE = 0xAA

LEN_SRC_ADDR = 4
LEN_DST_ADDR = 4
LEN_DATA_LENGTH = 2
LEN_HEADER_CHECKSUM = 2
LEN_DATA_CHECKSUM = 2


HOST_THIS = 1
HOST_X_COM_232I = 501
HOST_BSP = 601
HOST_ALL_XTM = 100
HOST_FIRST_INVERTER = 101
HOST_SECOND_INVERTER = 102
HOST_THIRD_INVERTER = 103

SERVICE_ID_READ_PROPERTY = 0x01
SERVICE_ID_WRITE_PROPERTY = 0x02

OBJECT_TYPE_DATALOG_TRANSFER = [0x01, 0x01]
OBJECT_TYPE_USER_INFO = [0x01, 0x00]
OBJECT_TYPE_PARAMETER = [0x02, 0x00]

OBJECT_ID_DIRECTORY_LIST = [0x00, 0x00, 0x00, 0x01]
OBJECT_ID_FILE_ACCESS = [0x00, 0x00, 0x00, 0x02]

INVALID_ACTION = [0x00, 0x00]
SD_START = [0x00, 0x21]
SD_DATABLOCK = [0x00, 0x22]
SD_ACK_CONTINUE = [0x00, 0x23]
SD_NACK_RETRY = [0x00, 0x24]
SD_ABORT = [0x00, 0x25]
SD_FINISH = [0x00, 0x26]

POID_VALUE = [0x01, 0x00]
POID_QSP_VALUE = [0x00, 0x05]

OBJECT_ID_BATTERY_VOLTAGE = 3000
OBJECT_ID_BATTERY_VOLTAGE_BSP = 7000
OBJECT_ID_BATTERY_CHARGE_CURRENT = 3005
OBJECT_ID_BATTERY_CURRENT = 7001
OBJECT_ID_BATTERY_POWER = 7003
OBJECT_ID_BATTERY_SOC = 7047

OBJECT_ID_PV1_POWER = 15011
OBJECT_ID_PV2_POWER = 15012

OBJECT_TRANSFERT = 3020
OBJECT_STATE_AUX_RELAY_1 = 3031
OBJECT_STATE_AUX_RELAY_2 = 3032
OBJECT_SOURCE_OF_LIMITATION = 3160
OBJECT_DEFINED_PHASE = 3089

OBJECT_INPUT_POWER = 3138
OBJECT_OUTPUT_POWER = 3139

OBJECT_INPUT_ACTIVE_POWER = 3136
OBJECT_OUTPUT_ACTIVE_POWER = 3137

OBJECT_ID_BATTERY_VOLTAGE_PRIORITY = 1297
OBJECT_ID_BATTERY_VOLTAGE_MIN = 1109
OBJECT_ID_BATTERY_VOLTAGE_MAX = 1121

OBJECT_ID_DATE = 5002

DATA_TYPE_FLOAT = 1
DATA_TYPE_SHORT_ENUM = 2
DATA_TYPE_INT32 = 3

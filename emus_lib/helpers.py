import importlib
import json
import logging
import sys
from logging import handlers
from emus_lib.constants import *


def crc_checksum(sentence):

    crc = 0x00
    poly = 0x18

    for char in sentence:
        data = ord(char)
        # print(str(data) + ' ' + char)
        bit_counter = 7

        while bit_counter > -1:
            feedback_bit = (crc ^ data) & 0x01

            if feedback_bit == 0x01:
                crc = crc ^ poly

            crc = (crc >> 1) & 0x7F

            if feedback_bit == 0x01:
                crc = crc | 0x80

            data = data >> 1

            bit_counter -= 1

    return crc


def util_class_instanciate(definition):
    module = importlib.import_module(definition['module'])
    class_ = getattr(module, definition['class_name'])
    return class_()


def enc(response):
    return json.dumps(response)


def dec(data):
    return json.loads(data)

def init_logging(name):
    logging.addLevelName(LOG_LEVEL_DEBUG_DEEPER, "DEBUG_DEEP")
    logger = get_logger(name)
    logger.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = handlers.RotatingFileHandler('/home/pi/homepy/log/'+name+'.log', maxBytes=(1048576*5), backupCount=7)
    c_format = logging.Formatter('%(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    return logger

def get_logger(name):
    return logging.getLogger(name)
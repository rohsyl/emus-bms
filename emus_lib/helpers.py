import importlib
import json
import logging


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


def get_logger(name):
    return logging.getLogger(name)
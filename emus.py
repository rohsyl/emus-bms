#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    :author: sylvain.roh
    :version:
        2022-04-29        sylvain.roh
            cleaning code
        2018-12-30 v0.1   sylvain.roh
            initial release
"""
import threading
import sys
from library.db import Db
from emus_lib.constants import *
from config.config import *
from emus_lib.helpers import *
from emus_lib.serial.emus import EmusSerial
from emus_lib.serial.locker import Locker
from logging import handlers

from emus_lib.queue.responsequeue import ResponseQueue

SER_PORT_NAME = EMUS_SERIAL_PORT

SEN_ONLY = [
    SEN_BV1,
    SEN_BV2,
]

SEN_RESPONSE_DEFINITION = {
    SEN_BV1: {'length': 1},
    SEN_BV2: {'length': 2},
}


def main():
    init_logging('emus')

    # wait until the emus.serial is unlocked
    while Locker.is_locked('emus'):
        pass

    # lock the emus.serial to avoid access to the serial by other process
    # and to tell other process that i'm using it
    Locker.lock('emus')

    q = ResponseQueue(SEN_RESPONSE_DEFINITION)

    serial = EmusSerial(SER_PORT_NAME, SEN_ONLY, SEN_RESPONSE_DEFINITION)
    serial.set_logger('emus')
    serial.open()

    serial.set_queue(q)

    thread = threading.Thread(target=serial.read, args=[False])
    thread.start()

    for request in SEN_RESPONSE_DEFINITION.keys():
        serial.write(request)

    while not q.is_queue_processed() and not q.has_timed_out():
        pass

    # Close serial connection
    serial.close()

    # release the lock to allow other process to use the emus.serial
    Locker.unlock('emus')

    items = q.get_items()

    values = {
        'total': None,
        'avg': None,
        'min': {
            'number': None,
            'value': None
        },
        'max': {
            'number': None,
            'value': None
        }
    }

    if 'BV1' in items:
        if len(items['BV1']) > 0:
            values['total'] = items['BV1'][0]['values']['TOTAL VOLTAGE']
            values['avg'] = items['BV1'][0]['values']['AVERAGE CELL VOLTAGE']

    if 'BV2' in items:
        bv2_values = []
        for d in items['BV2']:
            entry = d['values'];
            j = entry['CELL NUMBER OF FIRST CELL IN GROUP']
            while j < entry['SIZE OF GROUP'] + entry['CELL NUMBER OF FIRST CELL IN GROUP']:
                bv2_values.append(entry['INDIVIDUAL CELL VOLTAGE'][j - entry['CELL NUMBER OF FIRST CELL IN GROUP']])
                j += 1

        min_v = min(bv2_values)
        max_v = max(bv2_values)
        min_index = bv2_values.index(min_v)
        max_index = bv2_values.index(max_v)

        values['min']['value'] = min_v
        values['min']['number'] = min_index + 1
        values['max']['value'] = max_v
        values['max']['number'] = max_index + 1

    db = Db()
    db.set_logger('emus')

    db.open()
    db.insert_emus(values)
    db.close()

    sys.exit(0)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    :author: sylvain.roh
    :version:
        2022-04-29        sylvain.roh
            cleaning code
        2019-10-10 v0.1   sylvain.roh
            initial release
"""
import threading
import time
import sys
from library.db import Db
from config.config import *
from emus_lib.constants import *
from emus_lib.helpers import *
from emus_lib.serial.emus import EmusSerial
from emus_lib.serial.locker import Locker
from logging import handlers

from emus_lib.queue.responsequeue import ResponseQueue

SER_PORT_NAME = EMUS_SERIAL_PORT

SEN_ONLY = [
    SEN_BT1,
    SEN_BV1,
    SEN_BC1,
    SEN_CV1,
    SEN_BB1,
    SEN_DT1,
    SEN_OT1
]
if not NO_BT3:
    SEN_ONLY.append(SEN_BT3)

SEN_RESPONSE_DEFINITION = {
    SEN_BV1: {'length': 1},
    SEN_BT1: {'length': 1},
    SEN_BC1: {'length': 1},
    SEN_CV1: {'length': 1},
    SEN_BB1: {'length': 1},
    SEN_DT1: {'length': 1},
    SEN_OT1: {'length': 1}
}
if not NO_BT3:
    SEN_RESPONSE_DEFINITION[SEN_BT3] = {'length': 1}


def main():
    logger = init_logging('emus_broadcast')

    # wait until the emus.serial is unlocked
    while Locker.is_locked('emus'):
        pass

    # lock the emus.serial to avoid access to the serial by other process
    # and to tell other process that i'm using it
    Locker.lock('emus')

    q = ResponseQueue(SEN_RESPONSE_DEFINITION)

    serial = EmusSerial(SER_PORT_NAME, SEN_ONLY)
    serial.set_logger('emus_broadcast')

    try:
        serial.open()
    except Exception as e:
        logger.info('Error while open serial. End script.')
        logger.error(e)
        Locker.unlock('emus')
        sys.exit(0)

    if not serial.serial.isOpen():
        logger.info('No serial port. End script.')
        Locker.unlock('emus')
        sys.exit(0)

    serial.set_queue(q)

    thread = threading.Thread(target=serial.read_broadcast, args=[False])
    thread.start()

    while not q.is_queue_processed() and not q.has_timed_out():
        pass

    # Close serial connection
    serial.close()

    # release the lock to allow other process to use the emus.serial
    Locker.unlock('emus')

    items = q.get_items()

    # here you can send your data to a database...
    # see emus.py for an exemple.
    print(items)

    sys.exit(0)


if __name__ == '__main__':
    main()

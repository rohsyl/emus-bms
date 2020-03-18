
import threading
import time
from emus_lib.helpers import get_logger
from emus_lib.constants import *
from emus_lib.queue.responsequeue import ResponseQueue
from emus_lib.serial.emus import EmusSerial
from emus_lib.serial.locker import Locker
from .requesthandler import RequestHandler

SER_PORT_NAME = '/dev/ttyUSB1'

SEN_ONLY = [
    SEN_BT1,
    SEN_BT2,
    SEN_BV1,
    SEN_BV2,
    SEN_BB2
]

SEN_RESPONSE_DEFINITION = {
    SEN_BT1: {'length': 1},
    SEN_BV1: {'length': 1},
    SEN_BT2: {'length': 2},
    SEN_BV2: {'length': 2},
    SEN_BB2: {'length': 2}
    # SEN_VR1: {'length': 1},
}

logger = get_logger("service_socket")


class RequestDataHandler(RequestHandler):

    def __init__(self):
        RequestHandler.__init__(self)
        self.q = ResponseQueue(SEN_RESPONSE_DEFINITION, timeout=3)
        self.serial = EmusSerial(SER_PORT_NAME, SEN_ONLY, SEN_RESPONSE_DEFINITION)
        self.serial.set_logger('service_socket')
        self.serial.set_queue(self.q)
        self.thread = threading.Thread(target=self.serial.read, args=[False])

    def do(self):

        # wait until the emus.serial is unlocked
        while Locker.is_locked('emus'):
            pass

        # lock the emus.serial to avoid access to the serial by other process
        # and to tell other process that i'm using it
        Locker.lock('emus')

        # open the emus.serial
        self.serial.open()

        # start to listen fro responses
        self.thread.start()

        # send all requests
        for request in SEN_RESPONSE_DEFINITION.keys():
            self.serial.write(request)

        # wait until queue is fully processed or timed out
        while not self.q.is_queue_processed() and not self.q.has_timed_out():
            pass

        self.serial.close()

        # release the lock to allow other process to use the emus.serial
        Locker.unlock('emus')

    def response(self):
        return {
            'error': False,
            'message': 'getData',
            'data': self.q.get_items()
        }

    def end(self):

        self.serial.close()

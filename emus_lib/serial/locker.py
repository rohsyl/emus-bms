import os
from emus_lib.helpers import get_logger
from datetime import datetime, timedelta

logger = get_logger('service_socket')

LOCK_PATH = '/home/pi/homepy/'
LOCK_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOCK_TIMEOUT = 2


class Locker:

    @staticmethod
    def lock(what):
        f = open(Locker.__get_file_name(what), 'w')
        f.write(datetime.now().strftime(LOCK_DATE_FORMAT))
        f.close()

    @staticmethod
    def is_locked(what, timeout=LOCK_TIMEOUT):
        exists = os.path.isfile(Locker.__get_file_name(what))

        if exists:
            f = open(Locker.__get_file_name(what), 'r')
            s_date = f.read()

            if len(s_date) != len(LOCK_DATE_FORMAT):
                return False

            c_datetime = datetime.strptime(s_date, LOCK_DATE_FORMAT)

            time_should_end = c_datetime + timedelta(seconds=timeout)

            if time_should_end < datetime.now():
                return False
            else:
                return True

        else:
            return False

    @staticmethod
    def unlock(what):
        os.remove(Locker.__get_file_name(what))

    @staticmethod
    def __get_file_name(what):
        return LOCK_PATH + what + '.LOCK'

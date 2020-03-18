from library.db import Db
from library.constants import *


class EmusDataSyncJob:

    def process(self, job, data, logger='default'):
        db = Db()
        db.set_logger(logger)
        db.open()

        row = data[0]
        sentence = row['name']
        values = row['values']
        date = job[3]

        db.insert_emus_data(ID, sentence, values, date)

        db.close()
import mysql.connector
from library.constants import *
from emus_lib.helpers import get_logger
import logging
import json


class Db:

    def __init__(self, connection=None):
        logging.info('db init')
        self.db = None
        self.logger = logging

        self.host = DB_HOST
        self.user = DB_USER
        self.passwd = DB_PASS
        self.database = DB_NAME
        if connection is not None:
            if connection == 'sync':
                self.host = DB_SYNC_HOST
                self.user = DB_SYNC_USER
                self.passwd = DB_SYNC_PASS
                self.database = DB_SYNC_NAME
            elif connection == 'local':
                self.host = DB_LOCAL_HOST
                self.user = DB_LOCAL_USER
                self.passwd = DB_LOCAL_PASS
                self.database = DB_LOCAL_NAME


    def set_logger(self, name):
        self.logger = get_logger(name)

    def open(self):
        self.db = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            database=self.database
        )
        self.logger.info('db opened')

    def insert_data(self, parameter, source, value, date):
        cursor = self.db.cursor()
        sql = "INSERT INTO `datas` (`paramenter_nr`, `data_source`, `value`, `created_at`, `updated_at`) VALUES (%s, %s, %s, %s, %s);"
        val = (parameter, source, value, date, date)
        self.logger.info('Insert into db: ' + sql)
        self.logger.info(val)
        cursor.execute(sql, val)
        self.db.commit()
        cursor.close()
        del cursor

    def insert_daily_report(self, parameter, source, value, date):
        cursor = self.db.cursor()
        sql = "INSERT INTO `daily_reports` (`paramenter_nr`, `data_source`, `value`, `created_at`, `updated_at`) VALUES (%s, %s, %s, %s, %s);"
        val = (parameter, source, value, date, date)
        self.logger.info('Insert into db: ' + sql)
        self.logger.info(val)
        cursor.execute(sql, val)
        self.db.commit()
        cursor.close()
        del cursor

    def insert_emus(self, values):
        jsons = json.dumps(values)
        cursor = self.db.cursor()
        sql = "INSERT INTO `emus` (`json`, `created_at`, `updated_at`) VALUES ('" + jsons + "', NOW(), NOW());"
        self.logger.info('Insert into db: ' + sql)
        cursor.execute(sql)
        self.db.commit()
        cursor.close()
        del cursor

    def insert_emus_data(self, id, sentence, values, date):
        jsons = json.dumps(values)
        cursor = self.db.cursor()
        sql = "INSERT INTO `battery_data` (`battery_id`, `sentence`, `json`, `created_day`, `created_at`, `updated_at`) VALUES (%s, %s, %s, %s, %s, NOW());"
        val = (id, sentence, jsons, date, date)
        self.logger.info('Insert into db: Battery_id=' + str(id) + ' Sentence=' + sentence + ' Json=' + jsons + ' Date=' + date)
        cursor.execute(sql, val)
        self.db.commit()
        cursor.close()
        del cursor

    def close(self):
        self.logger.info('db closed')
        self.db.close()

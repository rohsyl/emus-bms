from library.db import Db
from emus_lib.helpers import *
from emus_lib.serial.locker import Locker

class DbSync:

    def __init__(self, queue='default'):
        self.queue = queue
        self.db_connection = 'sync'
        self.logger = None
        self.loggerName = 'default'

    def set_logger(self, name):
        self.loggerName = name
        self.logger = get_logger(name)

    def insertJob(self, payload):
        payload = enc(payload)
        db = Db(self.db_connection)
        db.set_logger(self.loggerName)
        db.open()
        cursor = db.db.cursor()
        sql = "INSERT INTO `jobs` (`payload`, `queue`, `attempt`, `created_at`) VALUES (%s, %s, %s, NOW());"
        val = (payload, self.queue, 0)
        cursor.execute(sql, val)
        db.db.commit()
        cursor.close()
        del cursor
        db.close()

    def processJobs(self):
        db = Db(self.db_connection)
        db.set_logger(self.loggerName)
        db.open()
        cursor = db.db.cursor()
        sql = "SELECT `id`, `payload`, `attempt`, `created_at` FROM `jobs` WHERE `queue` = %s;"
        val = (self.queue, )
        cursor.execute(sql, val)
        jobs = cursor.fetchall()
        remaining = len(jobs)
        for job in jobs:
            self.logger.info('Job remaining : ' + str(remaining))
            # relock to keep db locked while job is processing
            Locker.lock('db_jobs')
            try:
                # process job
                id = job[0]
                attempt = job[2]
                payload = dec(job[1])
                job_instance = util_class_instanciate(payload['job'])
                job_instance.process(job, payload['data'], self.loggerName)
                pass
            except Exception as e:
                # failed job
                attempt = attempt + 1
                sql = "UPDATE `jobs` SET attempt = %s WHERE id = %s;"
                val = (attempt, id)
                cursor.execute(sql, val)
                db.db.commit()
                raise e
                pass
            else:
                # success job
                sql = "DELETE FROM `jobs` WHERE id = %s;"
                val = (id, )
                cursor.execute(sql, val)
                db.db.commit()
                pass
            remaining = remaining - 1;
        cursor.close()
        del cursor
        db.close()



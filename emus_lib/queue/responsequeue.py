from copy import deepcopy
from datetime import datetime, timedelta


class ResponseQueue:

    def __init__(self, definition=None, timeout=None):
        self.timeout_define = False
        if definition is not None:
            self.init_queue(definition)
        if timeout is not None:
            self.timeout_define = True
            self.time_started = datetime.now()
            self.time_should_end = self.time_started + timedelta(seconds=timeout)
            print('started ' + str(self.time_started))
            print('should end ' + str(self.time_should_end))

    def put(self, key, value):
        if key in self.definition.keys():
            if self.definitionCounter[key]['length'] > 0:
                if key not in self.items.keys():
                    self.items[key] = []
                self.items[key].append(value)
                self.definitionCounter[key]['length'] -= 1
                self.__check_is_queue_processed()

    def get_items(self):
        return self.items

    def is_queue_processed(self):
        return self.processed

    def has_timed_out(self):
        if not self.timeout_define:
            return False
        else:
            if self.time_should_end < datetime.now():
                print('timed out')
                return True
            else:
                return False

    def init_queue(self, definition):
        self.definition = definition
        self.definitionCounter = deepcopy(self.definition)
        self.items = {}
        self.processed = False

    def __check_is_queue_processed(self):
        processed = True
        for name, item in self.definitionCounter.items():
            if item['length'] > 0:
                processed = False
                break
        self.processed = processed


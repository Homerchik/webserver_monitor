import logging
import time
from threading import Thread

from interfaces.storage import Storage
from tools.utils import necessary_tables, read_config
from workers.request_metrics import RequestMetrics
from wrappers.consumer import Consumer
from wrappers.producer import Producer


class Saver(Thread):
    def __init__(self, cons: Consumer, storage: Storage):
        super().__init__()
        self.storage = storage
        self.cons = cons
        self.configs = read_config()
        self.chunk_size = self.configs.get('application').get('chunk_size') or 10
        self.storage.prepare(necessary_tables())

    def run(self):
        while True:
            for msgs in self.cons.get_messages(self.chunk_size):
                if msgs:
                    logging.debug(f"Saving {len(msgs)} messages in PG")
                    self.storage.save(msgs)


class Publish(Thread):
    def __init__(self, req: RequestMetrics, producer: Producer):
        super().__init__()
        self.req = req
        self.producer = producer
        self.configs = read_config()
        self.update_interval = self.configs.get('application').get('update_interval') or 10
        self.last_req_time = 0

    def run(self):
        while True:
            if self.last_req_time + self.update_interval < time.time():
                logging.debug("Start of service availability check cycle")
                msg = self.req.request()
                self.last_req_time = time.time()
                self.producer.publish(topic="metrics", key=self.req.hostname, value=msg)

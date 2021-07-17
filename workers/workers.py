import logging
import time
from threading import Thread

from checker.request_metrics import RequestMetrics
from interfaces.storage import Storage
from tools.utils import necessary_tables
from wrappers.consumer import Consumer
from wrappers.producer import Producer


class Saver(Thread):
    def __init__(self, cons: Consumer, storage: Storage, read_delay: int = 10):
        super().__init__()
        self.storage = storage
        self.cons = cons
        self.read_delay = read_delay
        self.last_read = 0
        self.storage.prepare(necessary_tables())

    def run(self):
        while True:
            msgs = self.cons.get_messages()
            if msgs:
                logging.debug(f"Saving {len(msgs)} messages in PG")
                for msg in msgs:
                    self.storage.save(msg)


class Publish(Thread):
    def __init__(self, req: RequestMetrics, producer: Producer):
        super().__init__()
        self.req = req
        self.producer = producer
        self.last_req_time = 0

    def run(self):
        while True:
            if self.last_req_time + 10 < time.time():
                logging.debug("Start of service availability check")
                msg = self.req.request()
                self.last_req_time = time.time()
                self.producer.publish(topic="metrics", key=self.req.hostname, value=msg)

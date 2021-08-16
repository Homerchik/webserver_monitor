import logging
import time
from threading import Thread
from typing import List, Dict

from src.interfaces.storage import Storage
from src.tools.utils import necessary_tables, read_config
from src.workers.request_metrics import RequestMetrics
from src.wrappers.consumer import Consumer
from src.wrappers.producer import Producer


class Saver(Thread):
    def __init__(self, cons: Consumer, storage: Storage, tables: List[str] = None, is_daemon: bool = False,
                 config: Dict = None):
        super().__init__(daemon=is_daemon)
        self.storage = storage
        self.cons = cons
        self.configs = config or read_config()
        self.chunk_size = self.configs.get('application').get('chunk_size') or 10
        tables = tables or necessary_tables(config)
        self.storage.prepare(tables)

    def run(self):
        while True:
            for msgs in self.cons.get_messages(self.chunk_size):
                if msgs:
                    logging.debug(f"Saving {len(msgs)} messages in PG")
                    self.storage.save(msgs)


class Publish(Thread):
    def __init__(self, req: RequestMetrics, producer: Producer, is_daemon: bool = False, config: Dict = None):
        super().__init__(daemon=is_daemon)
        self.req = req
        self.producer = producer
        self.configs = config or read_config()
        self.update_interval = self.configs.get('application').get('update_interval') or 10
        self.last_req_time = 0

    def run(self):
        while True:
            logging.debug("Start of service availability check cycle")
            msg = self.req.request()
            self.last_req_time = time.time()
            self.producer.publish(topic="metrics", key=self.req.hostname, value=msg)
            time.sleep(self.update_interval)

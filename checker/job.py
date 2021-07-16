import re
import time
from threading import Thread
from typing import Dict

from requests import Session

from kafka_wrap.consumer import Consumer
from kafka_wrap.producer import Producer
from utils.http_wrapper import get


class Request:
    keys = ["ts", "hostname", "page", "status", "latency", "regex_valid"]

    def __init__(self, hostname: str, page: str, regexp: str = ""):
        self.hostname = hostname
        self.page = page
        self.url = f"http://{hostname}/{page}"
        self.regexp = re.compile(regexp)
        self.session = Session()

    def request(self) -> Dict:
        status, latency, regex = get(self.session, self.url, self.regexp)
        msg = {k: v for k, v in zip(self.keys, [int(time.time()), self.hostname, self.page, status, latency, regex])}
        return msg


class Store(Thread):
    def __init__(self, cons: Consumer, read_delay: int = 10):
        super().__init__()
        self.cons = cons
        self.read_delay = read_delay
        self.last_read = 0

    def run(self):
        while True:
            msg = self.cons.get_messages()
            print(f"{time.time()} got {msg}")


class Publish(Thread):
    def __init__(self, req: Request, producer: Producer):
        super().__init__()
        self.req = req
        self.producer = producer
        self.last_req_time = 0

    def run(self):
        while True:
            if self.last_req_time + 10 < time.time():
                msg = self.req.request()
                self.last_req_time = time.time()
                self.producer.publish(topic="metrics", key=self.req.hostname, value=msg)

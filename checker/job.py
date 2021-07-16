import re
import time
from threading import Thread
from typing import Tuple

from requests import Session

from kafka_wrap.producer import Producer
from utils.http_wrapper import get


class Job(Thread):
    def __init__(self, hostname: str, page: str, regexp: str = "", stop: bool = False):
        super().__init__()
        self.hostname = hostname
        self.page = page
        self.url = f"http://{hostname}/{page}"
        self.regexp = re.compile(regexp)
        self.session = Session()
        self.updates = []
        self.stop = stop
        self.last_req_time = 0
        self.last_send_time = 0

    def request(self) -> Tuple[int, int, bool]:
        ts = int(time.time())
        self.last_req_time = ts
        r = get(self.session, self.url, self.regexp)
        self.updates.append((ts, *r))
        return r

    def store(self) -> None:
        for m in self.updates:
            print(m)
        self.updates = []
        self.last_send_time = int(time.time())

    def run(self):
        while True:
            if self.last_send_time + 10 < time.time():
                self.store()
            if self.last_req_time + 5< time.time():
                self.request()
            if self.stop:
                if self.updates:
                    self.store()
                break


class Request:
    def __init__(self, hostname: str, page: str, regexp: str = ""):
        self.hostname = hostname
        self.page = page
        self.url = f"http://{hostname}/{page}"
        self.regexp = re.compile(regexp)
        self.session = Session()

    def request(self) -> str:
        status, latency, regex = get(self.session, self.url, self.regexp)
        msg = "|".join([str(x) for x in [int(time.time()), self.hostname, self.page, status, latency, regex]])
        return msg


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
                self.producer.publish(topic="metrics", key=self.req.hostname, value=" ".join(msg))

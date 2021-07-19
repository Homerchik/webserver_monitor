import re
from time import time
from typing import Dict

from requests import Session

from src.tools.utils import normalize
from src.wrappers.http_wrapper import get


class RequestMetrics:
    keys = ["ts", "hostname", "page", "status", "latency", "regex_valid"]

    def __init__(self, hostname: str, page: str, regexp: str = ""):
        self.hostname = hostname
        self.page = page
        self.url = f"http://{hostname}/{page}"
        self.regexp = re.compile(regexp)
        self.session = Session()

    def request(self) -> Dict:
        status, latency, regex = get(self.session, self.url, self.regexp)
        msg = {k: v for k, v in zip(self.keys,
                                    [int(time()), normalize(self.hostname), normalize(self.page) or None,
                                     status, int(latency / 1000), regex])}
        return msg

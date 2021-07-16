import re
from typing import Callable, Tuple

from requests import Session


class Job:
    def __init__(self, hostname: str, page: str, regexp: str = ""):
        self.hostname = hostname
        self.page = page
        self.url = f"http://{hostname}/{page}"
        self.regexp = re.compile(regexp)
        self.session = Session()

    def exec(self, fun: Callable) -> Tuple:
        pass

    def store(self, fun: Callable) -> None:
        pass

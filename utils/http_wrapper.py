import re
from typing import Tuple, Pattern

from requests import Session


def get(session: Session, url: str, regexp: Pattern = None) -> Tuple[int, int, bool]:
    r = session.get(url)
    match = len(re.findall(regexp, r.text)) > 0
    return r.status_code, r.elapsed.microseconds, match

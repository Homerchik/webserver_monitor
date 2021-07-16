import re
from typing import Tuple, Pattern

from requests import Session


def get(session: Session, url: str, regexp: Pattern = None) -> Tuple[int, int, bool]:
    r = session.get(url)
    if regexp:
        match = len(re.findall(regexp, r.text)) > 0
    else:
        match = True
    return r.status_code, r.elapsed, match

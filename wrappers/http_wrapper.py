import re
from typing import Tuple, Pattern

from requests import Session


def get(session: Session, url: str, regexp: Pattern = None) -> Tuple[int, int, bool]:
    try:
        r = session.get(url, timeout=60)
        match = len(re.findall(regexp, r.text)) > 0
    except Exception as e:
        print(e)
        return 0, 60000000, False

    return r.status_code, r.elapsed.microseconds, match

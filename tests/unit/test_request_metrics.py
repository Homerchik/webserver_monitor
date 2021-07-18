from datetime import timedelta
from random import randint, choice
from unittest.mock import Mock

import pytest

from tools.utils import normalize
from workers.request_metrics import RequestMetrics


@pytest.mark.parametrize("hostname, page", [("re.ex.ex", "ru/en/ru/es"),
                                            ("re-mi.com.dom", "main-page/es/dep_1")])
def test_request_returns_properly_formatted_msg(hostname, page):
    req_metrics = RequestMetrics(hostname, page, "")
    req_metrics.session = Mock(**{"get.return_value":
                                      Mock(text="ABCDE",
                                           status_code=choice([500, 200, 400]),
                                           elapsed=timedelta(microseconds=randint(10000, 200000)))})
    resp = req_metrics.request()
    assert resp.get("hostname") == normalize(hostname)
    assert resp.get("page") == normalize(page)
    assert resp.get("status")
    assert resp.get("ts")
    assert resp.get("regex_valid")
    assert resp.get("latency")

import re
from datetime import timedelta
from unittest.mock import Mock

import pytest

from utils.http_wrapper import get


class TestHttpWrapper:
    error_session = Mock(**{"get.return_value": Mock(text="Got an error", status_code=400,
                                                     elapsed=timedelta(microseconds=123))})
    success_session = Mock(**{"get.return_value": Mock(text="You are entering", status_code=200,
                                                       elapsed=timedelta(microseconds=1))})

    @pytest.mark.parametrize('session, regexp, expected', [(error_session, re.compile("Got"), (400, 123, True)),
                                                            (success_session, re.compile("are"), (200, 1, True)),
                                                            (error_session, re.compile("success"), (400, 123, False)),
                                                            (success_session, re.compile("number"), (200, 1, False))])
    def test_get_returns_correct_info(self, session, regexp, expected):
        resp = get(session, "xyz", regexp)
        assert resp == expected

import pytest

from tools.utils import normalize


@pytest.mark.parametrize("str, exp", [("some-host.ru", "some-host_ru"),
                                      ("me.io", "me_io"),
                                      ("i8i7.rambler.ru", "i8i7_rambler_ru")])
def test_table_names_normalization(str, exp):
    assert normalize(str) == exp

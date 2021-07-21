import pytest

from src.tools.utils import normalize, necessary_tables, flatten, create_job, read_config, validate_config

TEST_CONFIG = {"monitoring": {"x.y": {"main": {"regexp": "*"}, "about": {}},
                              "bish.com": {"": {}},
                              "bla-bla.io": {"en": {"regexp": "english"}}},
               "kafka": {"bootstrap_servers": []},
               "postgresql": {"host": "", "port": "", "user": "", "password": "", "dbname": ""}}

CONFIG_SCHEMA = {"monitoring": ""}


@pytest.mark.parametrize("str, exp", [("some-host.ru", "some-host_ru"),
                                      ("me.io", "me_io"),
                                      ("i8i7.rambler.ru", "i8i7_rambler_ru")])
def test_table_names_normalization(str, exp):
    assert normalize(str) == exp


@pytest.mark.parametrize("config, exp",
                         [(TEST_CONFIG, ["x_y", "bish_com", "bla-bla_io"]),
                          ({"monitoring": {}}, [])])
def test_necessary_tables(config, exp):
    tables = necessary_tables(config)
    assert len(tables) == len(exp)
    assert all((x in exp for x in tables))


def test_flatten():
    assert flatten([[1], [2], [3], [4]]) == [1, 2, 3, 4]


@pytest.mark.parametrize('config, hostname, exp',
                         [(TEST_CONFIG, "x.y", [("x.y", "main", "*"), ("x.y", "about", "")]),
                          (TEST_CONFIG, "bish.com", [("bish.com", "", "")]),
                          (TEST_CONFIG, "bla-bla.io", [("bla-bla.io", "en", "english")])])
def test_create_job(hostname, config, exp):
    act = create_job(hostname, config['monitoring'][hostname])
    assert act == exp


def test_read_config():
    config = read_config("configs/config.yaml")
    assert type(config) == dict


def test_validate_config():
    assert validate_config(CONFIG_SCHEMA, TEST_CONFIG)

import pytest

from src.workers.metrics_saver import PostgresMetrics


@pytest.mark.parametrize("table, fields, values, exp",
                         [("t", ["ts", "page", "status", "latency", "regex_valid"], [1, "p", 200, 1, True],
                           "INSERT INTO t(ts, page, status, latency, regex_valid) values(1, 'p', 200, 1, True)"),
                          ("t", ["ts"], [1], "INSERT INTO t(ts) values(1)"),
                          ("t", ["page", "regex_valid"], ["a", True],
                           "INSERT INTO t(page, regex_valid) values('a', True)"),
                          ("t", ["status", "latency"], [1, 2], "INSERT INTO t(status, latency) values(1, 2)")])
def test_insert(table, fields, values, exp):
    assert exp == PostgresMetrics.insert_line(table, fields, values)

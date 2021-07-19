import time

import pytest

from src.tools.utils import flatten
from src.wrappers.consumer import Consumer


@pytest.mark.parametrize('run_cycles', [2])
def test_message_received(run_cycles, config, pages, hostnames, run_publisher):
    cycles = 0
    consumer = Consumer("metrics", config=config)
    pages = flatten(list(pages.values()))
    for msgs in consumer.get_messages(5):
        if cycles > run_cycles:
            break
        cycles += 1
        assert len(msgs) == 5
        for msg in msgs:
            assert type(msg) == dict
            assert msg['ts']
            assert msg['hostname'] in hostnames
            assert msg['page'] in pages
            assert msg['status'] == 200
            assert msg['regex_valid'] in [True, False]


@pytest.mark.parametrize('run_cycles', [2])
def test_message_stored(run_cycles, config, hostnames, run_publisher, pg_connection, run_saver):
    start_time = time.time()
    cycles = 0
    bulk_size = 5
    messages = list()
    consumer = Consumer("metrics", config=config)
    for msgs in consumer.get_messages(bulk_size):
        if cycles > run_cycles:
            break
        messages.append(msgs)
        cycles += 1
    messages = flatten(messages)
    for host in hostnames:
        pg_connection.execute(select(host, int(start_time)))
    rez = pg_connection.fetch_data()
    messages_consumed = [(msg['ts'], msg['page'], msg['status'], msg['latency'], msg['regex_valid'])
                         for msg in messages]
    assert len(rez) == cycles * bulk_size
    assert messages_consumed == rez


def select(table: str, start: int) -> str:
    return f"SELECT * FROM {table} WHERE ts >= {start}"

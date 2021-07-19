from collections import namedtuple
from random import randint
from typing import Generator

import pytest

from src.wrappers.consumer import Consumer

Message = namedtuple("Message", ["value"])


def generate_message(number: int) -> Generator:
    for i in range(number):
        yield Message(randint(0, 1000))


class MockConsumer(Consumer):
    def __init__(self):
        self.consumer = (x for x in generate_message(200))


@pytest.mark.parametrize('bulk_size', [1, 10, 50, 100])
def test_messages_bulk_size(bulk_size):
    consumer = MockConsumer()
    for bulk in consumer.get_messages(bulk_size):
        assert bulk_size == len(bulk)

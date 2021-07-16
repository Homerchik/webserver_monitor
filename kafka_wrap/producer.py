import json
from typing import Callable, Dict, Any

from kafka import KafkaProducer


def json_to_binary(d: Dict) -> bytes:
    return bytes(json.dumps(d), encoding='utf8')


def to_binary(x: Any) -> bytes:
    return bytes(x, encoding='utf8')


class Producer(KafkaProducer):
    def __init__(self, value_serializer: Callable = json_to_binary, key_serializer: Callable = to_binary):
        super().__init__()
        self._producer = None
        self.connected = False
        self.value_serializer = value_serializer
        self.key_serializer = key_serializer
        self.__connect()

    def __connect(self):
        try:
            self._producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10),
                                           value_serializer=self.value_serializer,
                                           key_serializer=self.key_serializer)
            self.connected = True
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))

    def publish(self, topic: str, key: str, value: Dict):
        try:
            self._producer.send(topic, key=key, value=value)
            self._producer.flush()
        except Exception as ex:
            print('Exception in publishing message')
            print(str(ex))

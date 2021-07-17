import json
from typing import Callable, Dict

from kafka import KafkaConsumer


def binary_json_decode(msg) -> Dict:
    return json.loads(str(msg, encoding='utf8'))


class Consumer(KafkaConsumer):
    def __init__(self, topic: str, deserializer: Callable = binary_json_decode):
        super().__init__()
        self.connected = False
        self.topic = topic
        self.consumer = None
        self.deserializer = deserializer
        self.__connect()

    def __connect(self):
        try:
            self.consumer = KafkaConsumer(self.topic, auto_offset_reset='latest',
                                          bootstrap_servers=['localhost:9092'],
                                          api_version=(0, 10),
                                          value_deserializer=self.deserializer)
            self.connected = True
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))

    def get_messages(self, chunk_size: int = 3):
        msg = [m.value for m, i in zip(self.consumer, range(chunk_size+1)) if i]
        return msg
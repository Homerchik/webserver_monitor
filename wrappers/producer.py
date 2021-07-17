import logging
from typing import Callable, Dict

from kafka import KafkaProducer

from tools.utils import json_to_binary, to_binary


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
            logging.info("Connected to Kafka successfully")
        except Exception as e:
            logging.error(f'Exception while connecting Kafka {e}')

    def publish(self, topic: str, key: str, value: Dict):
        try:
            self._producer.send(topic, key=key, value=value)
            self._producer.flush()
            logging.debug("Update has been sent")
        except Exception as e:
            logging.error(f'Exception in publishing message {e}')

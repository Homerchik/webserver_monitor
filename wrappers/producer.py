import logging
from typing import Callable, Dict

from kafka import KafkaProducer

from tools.utils import json_to_binary, to_binary, read_config


class Producer(KafkaProducer):
    def __init__(self, value_serializer: Callable = json_to_binary, key_serializer: Callable = to_binary,
                 configs: Dict = None):
        super().__init__()
        self._producer = None
        self.connected = False
        self.value_serializer = value_serializer
        self.key_serializer = key_serializer
        self.__settings(configs)
        self.__connect()

    def __settings(self, configs):
        configs = configs or read_config()
        self.kafka_settings = configs.get('kafka').copy()
        if configs.get('kafka_prod'):
            self.kafka_settings.update(configs.get('kafka_prod'))
        assert self.kafka_settings
        self.kafka_settings["value_serializer"] = self.value_serializer
        self.kafka_settings["key_serializer"] = self.key_serializer

    def __connect(self):
        try:
            self._producer = KafkaProducer(**self.kafka_settings)
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

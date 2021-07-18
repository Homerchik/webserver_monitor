import logging
from typing import Callable

from kafka import KafkaConsumer

from tools.utils import normalize, binary_json_decode, read_config


class Consumer(KafkaConsumer):
    def __init__(self, topic: str, deserializer: Callable = binary_json_decode):
        super().__init__()
        self.connected = False
        self.topic = topic
        self.consumer = None
        self.deserializer = deserializer
        self.kafka_settings = None
        self.__settings()
        self.__connect()

    def __settings(self):
        configs = read_config()
        self.kafka_settings = configs.get('kafka')
        if configs.get('kafka_cons'):
            self.kafka_settings.update(configs.get('kafka_cons'))
        assert self.kafka_settings
        self.kafka_settings["value_deserializer"] = self.deserializer

    def __connect(self):
        try:
            self.consumer = KafkaConsumer(self.topic, **self.kafka_settings)
            self.connected = True
            logging.info("Connected to Kafka successfully.")
        except Exception as e:
            logging.error(f'Exception while connecting Kafka {e}')

    def get_messages(self, chunk_size: int = 20):
        bulk = list()
        for message in self.consumer:
            bulk.append(normalize(message.value))
            if len(bulk) > chunk_size - 1:
                yield bulk
                bulk = []

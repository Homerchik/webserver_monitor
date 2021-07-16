from kafka import KafkaProducer


class Producer(KafkaProducer):
    def __init__(self):
        super().__init__()
        self._producer = None
        self.connected = False
        self.connect()

    def connect(self):
        try:
            self._producer = KafkaProducer(bootstrap_servers=['localhost:9092'], api_version=(0, 10))
            self.connected = True
        except Exception as ex:
            print('Exception while connecting Kafka')
            print(str(ex))

    def publish(self, topic: str, key: str, value: str):
        try:
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            self._producer.send(topic, key=key_bytes, value=value_bytes)
            self._producer.flush()
        except Exception as ex:
            print('Exception in publishing message')
            print(str(ex))

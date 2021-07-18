import pytest
from kafka import KafkaConsumer

from tools.utils import read_config, create_job, flatten
from workers.request_metrics import RequestMetrics
from workers.workers import Publish
from wrappers.postgres import Postgres
from wrappers.producer import Producer

configs_rel_path = "../configs/config.yaml"


@pytest.fixture(scope='module')
def pg_connection():
    return Postgres()


@pytest.fixture(scope='module')
def kafka_consumer(config):
    configs = config.get('kafka')
    configs['auto_offset_reset'] = "latest"
    return KafkaConsumer("metrics", **configs)


@pytest.fixture(scope='module')
def run_publisher(config):
    configs = config.get('test').get('monitoring')
    j = flatten([create_job(hostname, settings) for hostname, settings in configs.items()])
    producer = Producer()
    publisher = [Publish(RequestMetrics(host, page, regexp), producer, is_daemon=True) for host, page, regexp in j]
    for p in publisher:
        p.start()

    yield


@pytest.fixture(scope='module')
def config():
    return read_config(configs_rel_path)


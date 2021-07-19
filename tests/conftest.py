from multiprocessing.context import Process
from typing import Dict

import pytest
from kafka import KafkaConsumer

from src.workers.metrics_saver import PostgresMetrics
from src.workers.request_metrics import RequestMetrics
from src.workers.workers import Publish, Saver
from src.wrappers.postgres import Postgres
from tests import flask_server
from src.tools.utils import read_config, create_job, flatten, normalize
from src.wrappers.consumer import Consumer
from src.wrappers.producer import Producer

configs_rel_path = "configs/config.yaml"


@pytest.fixture(scope='module')
def pg_connection(config):
    return Postgres(config)


@pytest.fixture(scope='module')
def kafka_consumer(config):
    configs = config.get('kafka').copy()
    configs['auto_offset_reset'] = "latest"
    return KafkaConsumer("metrics", **configs)


@pytest.fixture(scope='session')
def run_publisher(config, flask_service):
    configs = config.get('test').get('monitoring')
    j = flatten([create_job(hostname, settings) for hostname, settings in configs.items()])
    producer = Producer(configs=config)
    publisher = [Publish(RequestMetrics(host, page, regexp), producer, is_daemon=True, config=config)
                 for host, page, regexp in j]
    for p in publisher:
        p.start()
    yield


@pytest.fixture(scope='function')
def run_saver(hostnames, config):
    consumer = Consumer("metrics", config=config)
    storage = PostgresMetrics(config)
    job = Saver(consumer, storage, tables=hostnames, is_daemon=True, config=config)
    job.start()
    yield


@pytest.fixture(scope='session')
def config():
    return read_config(configs_rel_path)


@pytest.fixture(scope='function')
def hostnames(config):
    return [normalize(k) for k, _ in config.get('test').get('monitoring').items()]


@pytest.fixture(scope='function')
def pages(config) -> Dict[str, str]:
    return {normalize(host): [normalize(k)
                              for k in config.get('test').get('monitoring').get(host).keys()]
            for host in config.get('test').get('monitoring').keys()}


@pytest.fixture(scope='session')
def flask_service(config):
    p = Process(target=flask_server.run_server, args=(config,), daemon=True)
    p.start()
    yield

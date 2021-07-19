import logging

import click

from tools.log import init_logging
from tools.utils import build_conf_logging_path, build_conf_app_path, read_config
from workers.metrics_saver import PostgresMetrics
from workers.workers import Saver
from wrappers.consumer import Consumer


@click.command()
@click.option('--config-dir', prompt='Directory where application configs stored')
def run(config_dir):
    """Script that runs kafka consumer. It consumes metrics from Kafka and stores them to PG"""
    init_logging(build_conf_logging_path(config_dir))
    configs = read_config(build_conf_app_path(config_dir))
    consumer = Consumer("metrics", config=configs)
    storage = PostgresMetrics(configs)
    jobs = [Saver(consumer, storage, config=configs)]

    logging.info("Saver script init finished. Starting cycle...")
    for job in jobs:
        job.start()


if __name__ == "__main__":
    run()

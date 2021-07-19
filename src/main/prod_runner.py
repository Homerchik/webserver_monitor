import logging

import click

from src.tools.log import init_logging
from src.tools.utils import flatten, read_config, create_job, build_conf_logging_path, build_conf_app_path
from src.workers import RequestMetrics
from src.workers import Publish
from src.wrappers.producer import Producer


@click.command()
@click.option('--config-dir', prompt='Directory where application configs stored')
def run(config_dir):
    """Script that runs kafka producer. It checks webservices from config and push metric messages
       about services state to Kafka"""
    init_logging(build_conf_logging_path(config_dir))
    config = read_config(build_conf_app_path(config_dir))
    sites = config.get('monitoring').items()

    payload = flatten([create_job(hostname, settings) for hostname, settings in sites])
    producer = Producer(configs=config)
    work = [Publish(RequestMetrics(host, page, regexp), producer, config=config) for host, page, regexp in payload]

    logging.info(f"Metrics generator script init finished. Number of threads {len(work)}. Starting cycle...")
    for job in work:
        job.start()


if __name__ == "__main__":
    run()


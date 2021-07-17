import logging

from tools.log import init_logging
from workers.metrics_saver import PostgresMetrics
from workers.workers import Saver
from wrappers.consumer import Consumer

if __name__ == "__main__":
    init_logging()
    consumer = Consumer("metrics")
    storage = PostgresMetrics()
    jobs = [Saver(consumer, storage)]

    logging.info("Saver script init finished. Starting cycle...")
    for job in jobs:
        job.start()

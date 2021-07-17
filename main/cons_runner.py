from checker.workers import Saver, PostgresMetrics
from wrappers.consumer import Consumer

if __name__ == "__main__":
    consumer = Consumer("metrics")
    storage = PostgresMetrics()
    jobs = [Saver(consumer, storage)]

    for job in jobs:
        job.start()
from checker.job import Store
from kafka_wrap.consumer import Consumer

if __name__ == "__main__":
    consumer = Consumer("metrics")
    jobs = [Store(consumer)]

    for job in jobs:
        job.start()
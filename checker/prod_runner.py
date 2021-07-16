from checker.job import Publish, Request
from kafka_wrap.producer import Producer

if __name__ == "__main__":
    producer = Producer()
    jobs = [Publish(Request("exante.eu", "ru"), producer),
            Publish(Request("ya.ru", ""), producer),
            Publish(Request("google.com", ""), producer)]

    for job in jobs:
        job.start()


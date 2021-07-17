import logging
from typing import Dict, List, Tuple

import yaml

from tools.log import init_logging
from tools.utils import flatten
from workers.request_metrics import RequestMetrics
from workers.workers import Publish
from wrappers.producer import Producer


def create_job(hostname: str, host_settings: Dict) -> List[Tuple[str, str, str]]:
    jobs = []
    for page in host_settings.keys():
        jobs.append((hostname, page, host_settings.get(page).get("regexp") or ""))
    return jobs


if __name__ == "__main__":
    init_logging()

    with open("../configs/config.yaml", "r") as f:
        conf = yaml.safe_load(f)
    sites = conf.get('monitoring').items()

    payload = flatten([create_job(hostname, settings) for hostname, settings in sites])
    producer = Producer()
    work = [Publish(RequestMetrics(host, page, regexp), producer) for host, page, regexp in payload]

    logging.info(f"Metrics generator script init finished. Number of threads {len(work)}. Starting cycle...")
    for job in work:
        job.start()


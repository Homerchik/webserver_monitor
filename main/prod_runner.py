from typing import Dict, List, Tuple

import yaml

from checker.workers import Publish, Request
from tools.log import init_logging
from tools.utils import flatten
from wrappers.producer import Producer


def create_job(hostname: str, host_settings: Dict) -> List[Tuple[str, str, str]]:
    jobs = []
    for page in host_settings.keys():
        jobs.append((hostname, page, host_settings.get(page).get("regexp") or ""))
    return jobs


if __name__ == "__main__":
    init_logging()
    producer = Producer()
    with open("../configs/config.yaml", "r") as f:
        conf = yaml.safe_load(f)
    payload = flatten([create_job(hostname, settings) for hostname, settings in conf.get('monitoring').items()])
    work = [Publish(Request(host, page, regexp), producer) for host, page, regexp in payload]

    for job in work:
        job.start()


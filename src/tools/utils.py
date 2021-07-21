import json
import logging
from itertools import chain
from typing import Any, List, Dict, Tuple

import yaml
from inflection import parameterize


def read_config(path: str = "../configs/config.yaml") -> Dict:
    with open(path, "r") as f:
        return yaml.safe_load(f.read())


def build_conf_logging_path(dir_1: str) -> str:
    return f"{dir_1}/logging.yaml"


def build_conf_app_path(dir_1: str) -> str:
    return f"{dir_1}/config.yaml"


def normalize(s: Any) -> Any:
    if type(s) == str:
        return parameterize(s, separator="_")
    return s


def json_to_binary(d: Dict) -> bytes:
    return bytes(json.dumps(d), encoding='utf8')


def to_binary(x: Any) -> bytes:
    return bytes(x, encoding='utf8')


def binary_json_decode(msg) -> Dict:
    return json.loads(str(msg, encoding='utf8'))


def necessary_tables(config: Dict = None) -> List[str]:
    config = config or read_config()
    monitoring_settings = config.get('monitoring')
    return [normalize(host) for host in monitoring_settings.keys()]


def flatten(t):
    return list(chain.from_iterable(t))


def create_job(hostname: str, host_settings: Dict) -> List[Tuple[str, str, str]]:
    jobs = []
    for page in host_settings.keys():
        jobs.append((hostname, page, host_settings.get(page).get("regexp") or ""))
    return jobs


def validate_config(structure: Dict, config: Dict) -> bool:
    is_valid = True
    for key, value in structure.items():
        deep_config = config.get(key, None)
        if not deep_config:
            logging.error(f"No item for key {key} found!")
            is_valid = False
            break
        if type(value) == dict:
            if not validate_config(value, deep_config):
                return False
    return is_valid

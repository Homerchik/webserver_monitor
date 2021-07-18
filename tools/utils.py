import json
from typing import Any, List, Dict

import yaml
from inflection import parameterize


def read_config(path: str = "../configs/config.yaml") -> Dict:
    with open(path, "r") as f:
        return yaml.safe_load(f.read())


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


def necessary_tables(fpath: str = "../configs/config.yaml") -> List[str]:
    config = read_config(fpath)
    monitoring_settings = config.get('monitoring')
    return [normalize(host) for host in monitoring_settings.keys()]


def flatten(t):
    return [item for sublist in t for item in sublist]


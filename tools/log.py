import logging.config

from tools.utils import read_config


def init_logging(config_path: str = "../configs/logging.yaml"):
    config = read_config(config_path)
    logging.config.dictConfig(config)

import logging.config

from tools.utils import read_config


def init_logging():
    config = read_config("../configs/logging.yaml")
    logging.config.dictConfig(config)

import logging.config
import os

from src.tools.utils import read_config


def init_logging(config_path: str = "../configs/logging.yaml"):
    config = read_config(config_path)
    os.makedirs("./logs", exist_ok=True)
    logging.config.dictConfig(config)

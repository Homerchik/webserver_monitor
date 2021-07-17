import logging.config

import yaml


def init_logging():
    with open('../configs/logging.yaml', 'r') as f:
        config = yaml.safe_load(f)
        logging.config.dictConfig(config)

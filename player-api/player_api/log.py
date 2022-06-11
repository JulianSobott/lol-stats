import logging.config
from pathlib import Path

import yaml


def setup_logging():
    with open(Path(__file__).parent.joinpath("logging.yml"), "rt") as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def get_logger(name: str):
    return logging.getLogger(name)

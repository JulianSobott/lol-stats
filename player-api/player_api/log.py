import logging.config
from pathlib import Path


def setup_logging():
    logging.config.fileConfig(
        Path(__file__).parent.joinpath("logging.conf"), disable_existing_loggers=False
    )


def get_logger(name: str):
    return logging.getLogger(name)

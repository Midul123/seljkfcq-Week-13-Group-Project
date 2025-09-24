"""Script to run complete ELT pipeline."""

import logging

from utils import setup_logging
from extract import run_extract
from transform import run_transform
from load import run_load


def handler(event=None, context=None) -> None:
    """Handler function for lambda."""

    run_extract()
    run_transform()
    run_load()

    logging.info("ETL pipeline run successfully")


if __name__ == "__main__":
    setup_logging()
    handler()

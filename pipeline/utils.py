import os
from os import environ as ENV
import logging
import pyodbc

from dotenv import load_dotenv
import pandas as pd


def setup_logging() -> None:
    """Configures logging settings."""

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')


def check_for_tmp_folder() -> None:
    """Creates a folder for data outputs if it does not exists."""

    if not os.path.isdir('tmp'):
        logging.info("Creating tmp folder")
        os.mkdir('tmp')


def get_db_connection() -> pyodbc.Connection:
    """Returns a connection to database."""

    load_dotenv()
    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USER']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    conn = pyodbc.connect(conn_str)

    return conn

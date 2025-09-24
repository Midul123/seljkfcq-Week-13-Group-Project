"""Script for handling creation of parquet files."""

import os
import logging
import pyodbc

from dotenv import load_dotenv
import pandas as pd

from utils import setup_logging, get_db_connection

BASE_FOLDER = "c19-m3y-plants"


def setup_folders(base: str = BASE_FOLDER) -> None:
    """Creates folder structure for parquet files."""

    if not os.path.exists(base):
        os.mkdir(base)
        logging.info("Created base filepath.")

    if not os.path.exists(f"{base}/output"):
        os.mkdir(f"{base}/output")
        logging.info("Created output folder.")

    if not os.path.exists(f"{base}/input"):
        os.mkdir(f"{base}/input")
        logging.info("Created input folder.")

    if not os.path.exists(f"{base}/input/plant_readings"):
        os.mkdir(f"{base}/input/plant_readings")
        logging.info("Created input/plant_readings folder.")

    logging.info("Parquet files folder structure set up completed.")


def get_recording_data_df(conn: pyodbc.Connection) -> pd.DataFrame:
    """Returns recording data from database as dataframe."""

    query = """
        SELECT
            pr.plant_id,
            p.plant_name,
            p.city_id,
            c.city_name,
            ROUND(AVG(pr.temperature), 2) AS average_temperature,
            ROUND(AVG(pr.soil_moisture), 2) AS average_soil_moisture,
            COUNT(DISTINCT pr.last_watered) AS number_of_times_watered,
            COUNT(DISTINCT pr.recording_taken) AS number_of_recordings_taken,
            YEAR(MAX(pr.recording_taken)) AS year,
            MONTH(MAX(pr.recording_taken)) AS month,
            DAY(MAX(pr.recording_taken)) AS day
        FROM
            gamma.plant_reading pr
        LEFT JOIN
            gamma.plant p
        ON pr.plant_id = p.plant_id
        LEFT JOIN
            gamma.city c
        ON p.city_id = c.city_id
        GROUP BY
            pr.plant_id,
            p.plant_name,
            p.city_id,
            c.city_name
        ORDER BY pr.plant_id;
        """

    result = pd.read_sql(query, conn)

    logging.info("Retrieved all Recording data from database.")
    return result


def save_recordings_to_parquet(conn: pyodbc.Connection) -> None:
    """
    Creates the folder structure and saves recording data into parquet files.
    Returns dataframe with time partition columns.
    """

    df = get_recording_data_df(conn)
    setup_folders(BASE_FOLDER)
    df.to_parquet(
        path=f"{BASE_FOLDER}/input/plant_readings",
        partition_cols=['year', 'month', 'day']
    )

    logging.info("Created parquet structure & files.")


if __name__ == "__main__":

    setup_logging()

    conn = get_db_connection()
    save_recordings_to_parquet(conn)
    conn.close()

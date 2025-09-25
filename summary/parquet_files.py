"""Script for handling creation of parquet files."""

import os
import subprocess
import logging
import pyodbc
import awswrangler as wr
import boto3
import pandas as pd


from utils import setup_logging, get_db_connection


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

    logging.info("Retrieved all Recording data from database")
    return result


def boto_sesh():
    """Start a boto3 session"""
    return boto3.Session(aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                         aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"))


def save_recordings_to_parquet() -> None:
    """
    Creates the folder structure and saves recording data into parquet files.
    """
    b3 = boto_sesh()
    conn = get_db_connection()
    df = get_recording_data_df(conn)
    conn.close()

    wr.s3.to_parquet(df, path="s3://c19-seljkfcq-project/input/plant_readings",
                     dataset=True, boto3_session=b3, partition_cols=['year', 'month', 'day'])

    logging.info("Created parquet structure & files")


def reset_db():
    """Reset database after fetching and uploading data"""
    subprocess.run(["bash", "reset.sh"])


def handler(event=None, context=None) -> None:
    """Handler function for lambda."""
    save_recordings_to_parquet()
    reset_db()


if __name__ == "__main__":
    setup_logging()
    handler()

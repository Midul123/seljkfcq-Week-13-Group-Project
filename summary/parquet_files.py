"""Script for handling creation of parquet files."""

from os import environ as ENV
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
    b3_session = boto3.Session(profile_name="lambda-session")
    sts = b3_session.client("sts")
    response = sts.assume_role(
        RoleArn="arn:aws:iam::129033205317:role/seljkfcq-lambda-execution-role",
        RoleSessionName="lambda-session-1")

    return boto3.Session(aws_access_key_id=response['Credentials']['AccessKeyId'],
                         aws_secret_access_key=response['Credentials']['SecretAccessKey'],
                         aws_session_token=response['Credentials']['SessionToken'])


def save_recordings_to_parquet() -> None:
    """
    Creates the folder structure and saves recording data into parquet files.
    """
    b3 = boto_sesh()
    conn = get_db_connection()
    df = get_recording_data_df(conn)
    conn.close()

    wr.s3.to_parquet(df=df,
                     dataset=True,
                     path="s3://c19-seljkfcq-project/input/plant_readings",
                     partition_cols=['year', 'month', 'day'],
                     boto3_session=b3)

    logging.info("Created parquet structure & files")


def reset_db(conn: pyodbc.Connection):
    """Reset database after fetching and uploading data"""

    with conn.cursor() as cur:
        cur.execute("delete from gamma.plant_reading;")
        cur.execute("delete from gamma.plant;")
        cur.execute("delete from gamma.botanist;")
        cur.execute("delete from gamma.city;")
        conn.commit()


def handler(event=None, context=None) -> None:
    """Handler function for lambda."""
    save_recordings_to_parquet()
    conn = get_db_connection()
    reset_db(conn)
    conn.close()


if __name__ == "__main__":
    setup_logging()
    handler()

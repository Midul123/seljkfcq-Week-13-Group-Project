"""Retrieve Data from databases"""

import awswrangler as wr
import pandas as pd
import streamlit as st
import boto3
from os import environ as ENV
import pyodbc
from dotenv import load_dotenv


@st.cache_data()
def get_all_data():
    """Retrieve all data from database"""
    my_session = boto3.Session(
        aws_access_key_id=ENV.get("AWS_ACCESS_KEY"),
        aws_secret_access_key=ENV.get("AWS_SECRET_KEY"),
        region_name="eu-west-2"
    )

    query = """SELECT * FROM c19_seljkfcq_project
    """
    df = wr.athena.read_sql_query(
        query,
        database="c19-m3y-db",
        boto3_session=my_session)

    return pd.DataFrame(df)


@st.cache_data
def summary_data():

    b3 = boto3.Session()

    plant_data = wr.athena.read_sql_query(
        sql='select plant_name as "Plant names",avg(average_temperature) as "Avg Temp",avg(average_soil_moisture) as "Avg Soil moisture",avg(number_of_times_watered) as "Avg No. of Times Watered" from c19_seljkfcq_project group by plant_name;', database="c19-m3y-db", boto3_session=b3)

    return pd.DataFrame(plant_data)


def connect_to_rds():
    load_dotenv()
    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USER']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    return pyodbc.connect(conn_str)


@st.cache_data
def live_data():
    conn = connect_to_rds()
    query = """
    SELECT
        pr.*,
        p.plant_name,
        p.lat,
        p.lang,
        p.city_id,
        p.scientific_name,
        c.city_name,
        c.state_name
    FROM
        gamma.plant_reading pr
    LEFT JOIN
        gamma.plant p
    ON pr.plant_id = p.plant_id
    LEFT JOIN
        gamma.city c
    ON p.city_id = c.city_id;
    """

    recordings = pd.read_sql(query, conn)
    conn.close()

    recordings.set_index("reading_id")
    return recordings

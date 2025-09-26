"""Retrieve Data from databases"""

import awswrangler as wr
import pandas as pd
import streamlit as st
import boto3
from os import environ as ENV
import altair as alt


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

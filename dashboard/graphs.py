import streamlit as st
import altair as alt
import pandas as pd
import awswrangler as wr
import boto3


@st.cache_data
def summary_data():

    b3 = boto3.Session()

    plant_data = wr.athena.read_sql_query(
        sql='select plant_name as "Plant names",avg(average_temperature) as "Avg Temp",avg(average_soil_moisture) as "Avg Soil moisture",avg(number_of_times_watered) as "Avg No. of Times Watered" from c19_seljkfcq_project group by plant_name;', database="c19-m3y-db", boto3_session=b3)

    return pd.DataFrame(plant_data)

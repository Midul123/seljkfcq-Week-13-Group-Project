import streamlit as st
import altair as alt
import pandas as pd
import awswrangler as wr


@st.cache_data
def summary_data():
    plant_data = wr.athena.read_sql_query(
        sql='select plant_name as "Plant names",avg(average_temperature) as "Avg Temp",avg(average_soil_moisture) as "Avg Soil moisture",avg(number_of_times_watered) as "Avg No. of Times Watered" from c19_seljkfcq_project group by plant_name;', database="c19-m3y-db",)

    return pd.DataFrame(plant_data)

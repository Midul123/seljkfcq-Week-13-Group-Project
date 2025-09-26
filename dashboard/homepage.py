from get_all_data import live_data
from tables import temp_over_time, soil_over_time, latest_soil_recordings, chosen_plants_1, selected_plants_name_1, relevant_columns, add_delta_time_column
from charts import temp_over_time_chart, soil_over_time_chart, latest_soil_record, last_watered_chart
from os import environ as ENV
from dotenv import load_dotenv
import streamlit as st

import pyodbc
import pandas as pd
import altair as alt
alt.data_transformers.enable("vegafusion")


if __name__ == "__main__":
    all_data = live_data()
    temp_data = temp_over_time(all_data)
    soil_data = soil_over_time(all_data)
    latest_soil = latest_soil_recordings(soil_data)

    chosen_plants_temp = chosen_plants_1(
        temp_data, "Select Plants for Temperature Chart")
    selected = selected_plants_name_1(temp_data, chosen_plants_temp)
    st.altair_chart(temp_over_time_chart(selected))

    chosen_plants_soil = chosen_plants_1(
        soil_data, "Select Plants for Soil Chart")
    selected_2 = selected_plants_name_1(soil_data, chosen_plants_soil)
    st.altair_chart(soil_over_time_chart(selected_2))

    st.altair_chart(latest_soil_record(latest_soil))

    last_watered_data = relevant_columns(all_data)
    last_watered_data = add_delta_time_column(last_watered_data)
    st.altair_chart(last_watered_chart(last_watered_data))

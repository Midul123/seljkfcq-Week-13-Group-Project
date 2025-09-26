import awswrangler as wr
import pandas as pd
import streamlit as st
from os import environ as ENV
import altair as alt
from get_all_data import get_all_data
from charts import avg_moisture, create_line_chart_temp

if __name__ == "__main__":
    st.set_page_config(layout="wide")
    st.title("Daily Summary Dashboard")

    data = get_all_data()

    # Create two columns for filters
    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:
        available_months = sorted(data['month'].unique())
        selected_month = st.selectbox("Select Month", available_months)

    # Filter by selected month
    filtered_data = data[data['month'] == selected_month]

    with filter_col2:
        available_days = sorted(filtered_data['day'].unique())
        selected_day = st.selectbox("Select Day", available_days)

    # Final days
    filtered_data = filtered_data[filtered_data['day'] == selected_day]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Temperature")
        st.altair_chart(create_line_chart_temp(
            filtered_data).interactive(), use_container_width=True)

    with col2:
        st.subheader("Moisture")
        st.altair_chart(avg_moisture(
            filtered_data).interactive(), use_container_width=True)

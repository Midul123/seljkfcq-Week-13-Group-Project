import awswrangler as wr
import pandas as pd
import altair as alt
from get_all_data import live_data


def create_line_chart_temp(df: pd.DataFrame):
    chart = alt.Chart(df).mark_line().encode(
        x=alt.X("day:T", title="Day"),  # Time-aware axis
        y=alt.Y("average_temperature:Q", title="AVG Temperature"),
        color=alt.Color("plant_name:N", title="Plant Name"),
        tooltip=["day:T", "plant_name:N", "average_temperature:Q"]
    ).properties(
        title="Average Daily Temperature Over Time by Plant"
    )
    return chart


def avg_moisture(df: pd.DataFrame):
    """Line chart showing average soil moisture over time by plant"""
    chart2 = alt.Chart(df).mark_line().encode(
        x=alt.X("day:T", title="Day"),
        y=alt.Y("average_soil_moisture:Q", title="Average Moisture"),
        color=alt.Color("plant_name:N", title="Plant Name"),
        tooltip=["day:T", "plant_name:N", "average_soil_moisture:Q"]
    ).properties(
        title="Average Daily Moisture Over Time by Plant"
    )
    return chart2


def temp_over_time_chart(df):
    return alt.Chart(df, title="Temperature over Time").mark_line().encode(
        x="time:T",
        y="temperature:Q",
        color="plant_name:N"
    )


def soil_over_time_chart(df):

    return alt.Chart(df, title="Soil Moisture over Time").mark_line().encode(
        x="time:T",
        y="soil_moisture:Q",
        color="plant_name:N"
    )


def latest_soil_record(df):
    df["low_moisture"] = df["soil_moisture"] <= 30

    return alt.Chart(df.head(30), title="Latest Plant Soil Moisture Levels").mark_bar().encode(
        x=alt.X("plant_name").sort('y'),
        y="soil_moisture",
        color=alt.Color("low_moisture", legend=None)
    )


def last_watered_chart(last_watered_df):

    return alt.Chart(last_watered_df, title='Time since each plant was watered').mark_bar().encode(
        y=alt.Y('plant_name', title='Plant Name',
                axis=alt.Axis(labelLimit=200), sort='-x'),
        x=alt.X('hours_since_watered', title='Hours since watered'),
        tooltip=[alt.Tooltip('time_since_watered_formatted', title='Time since plant was watered'),
                 alt.Tooltip('soil_moisture', title='Soil moisture'),
                 alt.Tooltip('temperature', title='Temperature')]
    )

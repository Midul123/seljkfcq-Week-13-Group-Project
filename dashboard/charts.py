import awswrangler as wr
import pandas as pd
import altair as alt


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

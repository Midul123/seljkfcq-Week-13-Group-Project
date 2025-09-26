import streamlit as st
import awswrangler as wr
import pandas as pd
import datetime


def chosen_plants(df: pd.DataFrame, key_arg: str) -> list:
    '''chooses the plant(s) data you want to see'''
    all_plants = df['plant names'].unique()
    return st.multiselect(
        label='Plant selection', options=all_plants, default=all_plants, key=key_arg)


def selected_plants_name(df, chosen_plant_list: list) -> pd.DataFrame:
    '''filters data for chosen plants'''
    return df[df['plant names'].isin(chosen_plant_list)]


def chosen_plants_1(df: pd.DataFrame, key_arg: str) -> list:
    '''chooses the plants(s) data you want to see'''
    all_plants = df['plant_name'].unique()
    return st.multiselect(
        label='Plant selection', options=all_plants, default=all_plants, key=key_arg)


def selected_plants_name_1(df, chosen_plant_list: list) -> pd.DataFrame:
    '''filters data for chosen plants'''
    return df[df['plant_name'].isin(chosen_plant_list)]


def selected_plants_temp(df, chosen_temp: list) -> pd.DataFrame:
    '''filters data for chosen plants'''
    return df[df['avg temp'].apply(lambda x: x > chosen_temp)]


def selected_plants_soil(df, chosen_soil: list) -> pd.DataFrame:
    '''filters data for chosen plants'''
    return df[df['avg soil moisture'].apply(lambda x: x > chosen_soil)]


def temp_over_time(df):
    temp_recordings = pd.concat(
        [df["plant_name"], pd.to_datetime(df["recording_taken"]), df["temperature"]], axis=1)

    temp_recordings = pd.concat(
        [df["plant_name"], pd.to_datetime(df["recording_taken"]), df["temperature"]], axis=1)
    temp_recordings = temp_recordings.rename(
        columns={"recording_taken": "time"})
    temp_recordings["time"] = temp_recordings["time"].dt.floor('min')
    return temp_recordings


def soil_over_time(df):
    soil_recordings = pd.concat(
        [df["plant_name"], pd.to_datetime(df["recording_taken"]), df["soil_moisture"]], axis=1)

    soil_recordings = soil_recordings.rename(
        columns={"recording_taken": "time"})
    soil_recordings["time"] = soil_recordings["time"].dt.floor('min')

    soil_recordings.loc[soil_recordings["soil_moisture"]
                        < 0, "soil_moisture"] = None
    return soil_recordings


def latest_soil_recordings(df):
    filter_no_negative_recordings = df["soil_moisture"] >= 0

    latest_soil_recordings = df[filter_no_negative_recordings]
    latest_soil_recordings = latest_soil_recordings.sort_values(
        "time").groupby("plant_name").tail(1)
    latest_soil_recordings = latest_soil_recordings.sort_values(
        "soil_moisture")
    return latest_soil_recordings


def relevant_columns(df):
    last_watered_df = df[['last_watered',
                          'plant_name', 'soil_moisture', 'temperature']]
    last_watered_df = last_watered_df.sort_values(
        "last_watered").groupby("plant_name").tail(1)
    return last_watered_df


def format_timedelta(delta: datetime.timedelta) -> str:
    """ Formats timedelta into a more readable format. """
    seconds_in_day = 86400
    seconds_in_hour = 3600
    seconds_in_minute = 60

    seconds = int(delta.total_seconds())

    days = seconds // seconds_in_day
    hours = (seconds % seconds_in_day) // seconds_in_hour
    minutes = (seconds % seconds_in_hour) // seconds_in_minute

    return f'{days} days, {hours} hours, {minutes} minutes'


def add_delta_time_column(last_watered_df):
    now = datetime.datetime.now()

    last_watered_df['hours_since_watered'] = (
        now - last_watered_df['last_watered']).dt.total_seconds() / 3600
    last_watered_df['time_since_watered_formatted'] = (
        now - last_watered_df['last_watered']).apply(format_timedelta)
    last_watered_df.loc[last_watered_df['soil_moisture']
                        < 0, 'soil_moisture'] = None
    return last_watered_df

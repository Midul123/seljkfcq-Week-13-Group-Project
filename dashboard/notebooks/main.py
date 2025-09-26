import streamlit as st
import awswrangler as wr
import pandas as pd

from graphs import summary_data


def chosen_plants(df: pd.DataFrame, key_arg: str) -> list:
    '''chooses the truck(s) data you want to see'''
    all_plants = df['plant names'].unique()
    return st.multiselect(
        label='Plant selection', options=all_plants, default=all_plants, key=key_arg)


def selected_plants_name(df, chosen_plant_list: list) -> pd.DataFrame:
    '''filters data for chosen trucks'''
    return df[df['plant names'].isin(chosen_plant_list)]


def selected_plants_temp(df, chosen_temp: list) -> pd.DataFrame:
    '''filters data for chosen trucks'''
    return df[df['avg temp'].apply(lambda x: x > chosen_temp)]


def selected_plants_soil(df, chosen_soil: list) -> pd.DataFrame:
    '''filters data for chosen trucks'''
    return df[df['avg soil moisture'].apply(lambda x: x > chosen_soil)]


if __name__ == "__main__":
    data = summary_data()
    chosen = chosen_plants(data, "Plant Selector")
    if len(chosen) > 0:
        new_df = selected_plants_name(data, chosen)
        temp = temp_threshold = st.number_input(
            "Enter a minimum temperature to filter by (°C):", min_value=0, max_value=100)
        soil = st.number_input(
            "Enter a minimum temperature to filter by (mm):")
        if temp:
            new_df = selected_plants_temp(new_df, temp)
        if soil:
            new_df = selected_plants_soil(new_df, soil)

        st.dataframe(new_df)
    else:
        st.write('Choose at least one plant')

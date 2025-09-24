'''Get the extracted data clean it fixing columns and types then save it'''

# pylint: disable=line-too-long

import pandas as pd


def add_columns(df):
    "Some of these columns was stored in a dict under one column extrapolated them out"
    df['lat'] = df['origin_location'].apply(lambda x: x['latitude'])
    df['long'] = df['origin_location'].apply(lambda x: x['longitude'])
    df['city'] = df['origin_location'].apply(lambda x: x['city'])
    df['country'] = df['origin_location'].apply(lambda x: x['country'])
    df['botanist_name'] = df['botanist'].apply(lambda x: x['name'])
    df['email'] = df['botanist'].apply(lambda x: x['email'])
    df['phone'] = df['botanist'].apply(lambda x: x['phone'])
    return df


def change_type_to_date(df):
    "changed types of 2 columns to datetime"
    df['last_watered'] = pd.to_datetime(df['last_watered'])
    df['recording_taken'] = pd.to_datetime(df['recording_taken'])
    return df


def drop_columns(df):
    "remove unnecessary columns"
    df = df.drop(columns=['origin_location', 'botanist', 'images'])
    return df


def round_floats_2dp(df):
    "round all floats to 2dp"
    df['soil_moisture'] = df['soil_moisture'].round(2)
    df['temperature'] = df['temperature'].round(2)
    df['lat'] = df['lat'].round(2)
    df['long'] = df['long'].round(2)
    return df


def clean_phone_numbers(df):
    """ Transforms the phone numbers so that they all follow the same pattern. """
    df['phone'] = df['phone'].str.replace(
        r'(\(|\))', '', regex=True).replace(r'x(.*)', '', regex=True).replace(r'^1-', '', regex=True)
    df['phone'] = df['phone'].str.rstrip(
        ' ').str.replace('.', '-').str.replace(' ', '-')
    return df


if __name__ == "__main__":
    plants_df = pd.read_json("plants.json")
    cleaned_df = add_columns(plants_df)
    cleaned_df = change_type_to_date(cleaned_df)
    cleaned_df = drop_columns(cleaned_df)
    cleaned_df = round_floats_2dp(cleaned_df)
    cleaned_df = clean_phone_numbers(cleaned_df)
    cleaned_df.to_csv("cleaned_plants_data.csv", index=False)

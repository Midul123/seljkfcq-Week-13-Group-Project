"""Script to clean extracted data, fixing columns and types."""

# pylint: disable=line-too-long

import re
import logging

import pandas as pd

from utils import setup_logging


def add_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Extract required column from combined column in data."""

    df['lat'] = df['origin_location'].apply(lambda x: x['latitude'])
    df['long'] = df['origin_location'].apply(lambda x: x['longitude'])
    df['city'] = df['origin_location'].apply(lambda x: x['city'])
    df['country'] = df['origin_location'].apply(lambda x: x['country'])
    df['botanist_name'] = df['botanist'].apply(lambda x: x['name'])
    df['email'] = df['botanist'].apply(lambda x: x['email'])
    df['phone'] = df['botanist'].apply(lambda x: x['phone'])

    logging.info("Extracted required columns from combined columns")
    return df


def change_type_to_date(df: pd.DataFrame) -> pd.DataFrame:
    """Change data types of columns to datetime."""

    df['last_watered'] = pd.to_datetime(df['last_watered'])
    df['recording_taken'] = pd.to_datetime(df['recording_taken'])

    logging.info("Changed data types of columns to be datetime")
    return df


def drop_unneeded_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove unnecessary columns."""

    df = df.drop(columns=['origin_location', 'botanist', 'images'])
    logging.info("Removed unnecessary columns")
    return df


def round_floats_2dp(df: pd.DataFrame) -> pd.DataFrame:
    """Round all columns with float values to 2dp."""

    df['soil_moisture'] = df['soil_moisture'].round(2)
    df['temperature'] = df['temperature'].round(2)
    df['lat'] = df['lat'].round(2)
    df['long'] = df['long'].round(2)

    logging.info("Rounded all columns with floats")
    return df


def clean_phone_numbers(df: pd.DataFrame) -> pd.DataFrame:
    """Transforms phone numbers to have a consistent pattern."""

    df['phone'] = df['phone'].str.replace(
        r'(\(|\))', '', regex=True).replace(r'x(.*)', '', regex=True).replace(r'^1-', '', regex=True)
    df['phone'] = df['phone'].str.rstrip(
        ' ').str.replace('.', '-').str.replace(' ', '-')

    logging.info("Fix phone number formats")
    return df


def remove_brackets_from_scientific_name(df: pd.DataFrame) -> pd.DataFrame:
    """Remove brackets in scientific names."""

    df['scientific_name'] = df['scientific_name'].apply(
        lambda x: str(x) if pd.notna(x) else x)
    df['scientific_name'] = df['scientific_name'].str.replace(
        r'\[|\]', '', regex=True)

    logging.info("Removed brackets in scientific names")
    return df


def clean_emails(df: pd.DataFrame) -> pd.DataFrame:
    """Clean extra special characters in email column."""

    df['email'] = df['email'].str.replace(
        r'^[\W_]+', '', regex=True).replace(
        r'[\W_]+@', '@', regex=True)
    df['email'] = df['email'].apply(
        lambda x: re.sub(r'([\W_])\1+', r'\1', x))

    logging.info("Clean email formats")
    return df


def save_data_as_csv(df: pd.DataFrame) -> None:
    """Save the cleaned plant data as a CSV file."""

    df.to_csv("/tmp/cleaned_plants_data.csv", index=False)
    logging.info(
        "Created CSV file to store cleaned plant data: /tmp/cleaned_plants_data.csv")


def run_transform() -> None:
    """Run transform script."""

    plants_df = pd.read_json("/tmp/plants.json")
    cleaned_df = add_columns(plants_df)
    cleaned_df = change_type_to_date(cleaned_df)
    cleaned_df = drop_unneeded_columns(cleaned_df)
    cleaned_df = round_floats_2dp(cleaned_df)
    cleaned_df = clean_phone_numbers(cleaned_df)
    cleaned_df = remove_brackets_from_scientific_name(cleaned_df)
    cleaned_df = clean_emails(cleaned_df)
    logging.info("Transform script run successfully")


if __name__ == "__main__":
    setup_logging()
    run_transform()

""" This file runs the whole ETL script """

# pylint: disable=line-too-long, unused-argument

import asyncio
import pandas as pd


from extract import main, load_data_to_json
from transform import add_columns, change_type_to_date, drop_columns, round_floats_2dp, clean_phone_numbers, remove_brackets_from_scientific_name, clean_emails
from load import get_db_connection, get_all_data, upload_to_botanist_table, upload_to_city_table, upload_to_plant_readings_table, upload_to_plant_table


def handler(event=None, context=None) -> None:
    """ Handler function for lambda. """
    # Extract
    plant_data = asyncio.run(main())
    plant_data = [x for x in plant_data if x is not None]
    load_data_to_json(plant_data)

    # Transform
    plants_df = pd.read_json("plants.json")
    cleaned_df = add_columns(plants_df)
    cleaned_df = change_type_to_date(cleaned_df)
    cleaned_df = drop_columns(cleaned_df)
    cleaned_df = round_floats_2dp(cleaned_df)
    cleaned_df = clean_phone_numbers(cleaned_df)
    cleaned_df = remove_brackets_from_scientific_name(cleaned_df)
    cleaned_df = clean_emails(cleaned_df)
    cleaned_df.to_csv("cleaned_plants_data.csv", index=False)

    # Load
    con = get_db_connection()
    all_data = get_all_data()
    upload_to_city_table(con, all_data)
    upload_to_botanist_table(con, all_data)
    upload_to_plant_table(con, all_data)
    upload_to_plant_readings_table(con, all_data)


if __name__ == "__main__":
    handler()

"""Script to load data to Microsoft SQL Server."""

# pylint: disable=line-too-long, c-extension-no-member

import logging

import pandas as pd
import pyodbc

from utils import setup_logging, get_db_connection


def get_all_data() -> pd.DataFrame:
    """Return all data from CSV file as a dataframe."""

    df = pd.read_csv("/tmp/cleaned_plants_data.csv")
    return df


def upload_to_city_table(conn: pyodbc.Connection, df: pd.DataFrame) -> None:
    """Upload data to city table."""

    df = df[["city", "country"]].drop_duplicates()
    rows = list(df.itertuples(index=False))

    with conn.cursor() as cur:
        for row in rows:
            cur.execute(
                """
                IF NOT EXISTS (
                    SELECT 1
                    FROM city
                    WHERE city_name = ?
                    AND state_name = ?
                )
                BEGIN
                    INSERT INTO city (city_name, state_name)
                    VALUES (?, ?)
                END
                """,
                (row.city, row.country, row.city, row.country)
            )

    logging.info("Inserted data into city table")


def upload_to_botanist_table(conn: pyodbc.Connection, df: pd.DataFrame) -> None:
    """Upload data to botanist table."""

    df = df[["botanist_name", "email", "phone"]].drop_duplicates()
    rows = list(df.itertuples(index=False))

    with conn.cursor() as cur:
        for row in rows:
            cur.execute(
                """
                IF NOT EXISTS (
                    SELECT 1
                    FROM botanist
                    WHERE botanist_name = ?
                    AND botanist_email = ?
                    AND botanist_phone = ?
                )
                BEGIN
                    INSERT INTO botanist (botanist_name, botanist_email, botanist_phone)
                    VALUES (?, ?, ?)
                END
                """,
                (row.botanist_name, row.email,
                 row.phone, row.botanist_name, row.email, row.phone)
            )

    logging.info("Inserted data into botanist table")


def get_all_plant_id_name(conn: pyodbc.Connection) -> pd.DataFrame:
    """Return all plant IDs & names as dataframe."""

    query = "SELECT plant_id, plant_name FROM plant"
    df_plant = pd.read_sql(query, conn)
    return df_plant.drop_duplicates(subset=["plant_name"])


def get_all_city_id_name(conn: pyodbc.Connection) -> pd.DataFrame:
    """Return all city IDs & names as dataframe."""

    query = "SELECT city_id, city_name FROM city"
    df_city = pd.read_sql(query, conn)
    return df_city


def get_all_botanist_id_name(conn: pyodbc.Connection) -> pd.DataFrame:
    """Return all botanist IDs & names as dataframe."""

    query = "SELECT botanist_id, botanist_name FROM botanist"
    df_botanist = pd.read_sql(query, conn)
    return df_botanist.drop_duplicates(subset=["botanist_name"])


def upload_to_plant_table(conn: pyodbc.Connection, df: pd.DataFrame) -> None:
    """Upload data to plant table."""

    df = df[["name", "lat", "long", "city",
             "scientific_name"]].drop_duplicates()

    # Add city_name to dataframe based on city_id
    city_id = get_all_city_id_name(conn)
    df = df.merge(city_id, how='inner', left_on='city',
                  right_on='city_name')

    df["scientific_name"] = df["scientific_name"].astype(
        str).replace("nan", None)
    rows = list(df.itertuples(index=False))

    with conn.cursor() as cur:
        for row in rows:
            cur.execute(
                """
                IF NOT EXISTS (
                    SELECT 1
                    FROM plant
                    WHERE plant_name = ?
                )
                BEGIN
                    INSERT INTO plant (plant_name, lat, lang, city_id, scientific_name)
                    VALUES (?, ?, ?, ?, ?)
                END
                """,
                (row.name, row.name, row.lat, row.long,
                 row.city_id, row.scientific_name)
            )

    logging.info("Inserted data into plant table")


def upload_to_plant_reading_table(conn: pyodbc.Connection, df: pd.DataFrame) -> None:
    """Upload data to plant_reading table."""

    df = df[["name", "temperature", "last_watered", "soil_moisture",
             "botanist_name", "recording_taken"]].drop_duplicates()

    # Add plant_name to dataframe based on plant_id
    plant_id = get_all_plant_id_name(conn)
    df = df.merge(plant_id, how='inner', left_on='name',
                  right_on='plant_name')

    # Add botanist_name to dataframe based on botanist_id
    botanist_id = get_all_botanist_id_name(conn)
    df = df.merge(botanist_id, how='inner', left_on='botanist_name',
                  right_on='botanist_name')

    rows = list(df.itertuples(index=False))

    with conn.cursor() as cur:
        for row in rows:
            cur.execute(
                """
                    INSERT INTO plant_reading (plant_id, botanist_id, temperature, last_watered, soil_moisture, recording_taken)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                (row.plant_id, row.botanist_id,
                 row.temperature, row.last_watered, row.soil_moisture, row.recording_taken)
            )

    logging.info("Inserted data into plant_reading table")


def run_load() -> None:
    """Run load script."""

    conn = get_db_connection()
    data = get_all_data()
    upload_to_city_table(conn, data)
    upload_to_botanist_table(conn, data)
    upload_to_plant_table(conn, data)
    upload_to_plant_reading_table(conn, data)
    conn.close()

    logging.info("Load script run successfully")


if __name__ == "__main__":
    setup_logging()
    run_load()

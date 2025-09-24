"""Script to load data to microsoft sql server"""

# pylint: disable=line-too-long, c-extension-no-member

from os import environ as ENV
from dotenv import load_dotenv
import pyodbc
import pandas as pd


def get_db_connection() -> pyodbc.Connection:
    """get db connection"""
    load_dotenv()
    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USER']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    conn = pyodbc.connect(conn_str)

    return conn


def get_all_data() -> pd.DataFrame:
    """Get all data from csv file"""
    data = pd.read_csv("cleaned_plants_data.csv")
    return data


def upload_to_city_table(conn: pyodbc.Connection, df: pd.DataFrame):
    """Uploads data to city table"""
    df = df[["city", "country"]].drop_duplicates()
    rows = list(df.itertuples(index=False))

    with conn.cursor() as cur:
        for row in rows:
            cur.execute(
                """
                IF NOT EXISTS (
                    SELECT 1 FROM city WHERE city_name = ? AND state_name = ?
                )
                BEGIN
                    INSERT INTO city (city_name, state_name) VALUES (?, ?)
                END
                """,
                (row.city, row.country, row.city, row.country)
            )


def upload_to_botanist_table(conn: pyodbc.Connection, df: pd.DataFrame):
    """Uploads data to botanist table"""
    df = df[["botanist_name", "email", "phone"]].drop_duplicates()
    rows = list(df.itertuples(index=False))

    with conn.cursor() as cur:
        for row in rows:
            cur.execute(
                """
                IF NOT EXISTS (
                    SELECT 1 FROM botanist WHERE botanist_name = ? AND botanist_email = ? AND botanist_phone = ?
                )
                BEGIN
                    INSERT INTO botanist (botanist_name, botanist_email, botanist_phone) VALUES (?, ?, ?)
                END
                """,
                (row.botanist_name, row.email,
                 row.phone, row.botanist_name, row.email, row.phone)
            )


def get_all_city_id(conn: pyodbc.Connection) -> pd.DataFrame:
    """Get all city id to map to city names"""
    query = "SELECT city_id, city_name FROM city"
    df_city = pd.read_sql(query, conn)
    return df_city


def upload_to_plant_table(conn: pyodbc.Connection, df: pd.DataFrame):
    """Uploads data to plant table"""
    df = df[["name", "lat", "long", "city",
             "scientific_name"]].drop_duplicates()
    city_id = get_all_city_id(conn)
    df = df.merge(city_id, how='inner', left_on='city',
                  right_on='city_name')  # Get corresponding ids
    df["scientific_name"] = df["scientific_name"].astype(
        str).replace("nan", None)
    rows = list(df.itertuples(index=False))

    with conn.cursor() as cur:
        for row in rows:
            cur.execute(
                """
                IF NOT EXISTS (
                    SELECT 1 FROM plant WHERE plant_name = ?
                )
                BEGIN
                    INSERT INTO plant (plant_name, lat, lang, city_id, scientific_name) VALUES (?, ?, ?, ?, ?)
                END
                """,
                (row.name, row.name, row.lat, row.long,
                 row.city_id, row.scientific_name)
            )


def get_all_plant_id(conn: pyodbc.Connection) -> pd.DataFrame:
    """Get all plant id to map to city names"""
    query = "SELECT plant_id, plant_name FROM plant"
    df_plant = pd.read_sql(query, conn)
    return df_plant.drop_duplicates(subset=["plant_name"])


def get_all_botanist_id(conn: pyodbc.Connection) -> pd.DataFrame:
    """Get all botanist id to map to city names"""
    query = "SELECT botanist_name, botanist_id FROM botanist"
    df_botanist = pd.read_sql(query, conn)
    return df_botanist.drop_duplicates(subset=["botanist_name"])


def upload_to_plant_readings_table(conn: pyodbc.Connection, df: pd.DataFrame):
    """Uploads data to plant readings table"""
    df = df[["name", "temperature", "last_watered", "soil_moisture",
             "botanist_name", "recording_taken"]].drop_duplicates()
    plant_id = get_all_plant_id(conn)
    botanist_id = get_all_botanist_id(conn)

    df = df.merge(plant_id, how='inner', left_on='name',
                  right_on='plant_name')  # Get corresponding ids
    df = df.merge(botanist_id, how='inner', left_on='botanist_name',
                  right_on='botanist_name')

    rows = list(df.itertuples(index=False))

    with conn.cursor() as cur:
        for row in rows:
            cur.execute(
                """
                    INSERT INTO plant_reading (plant_id, botanist_id, temperature, last_watered, soil_moisture, recording_taken) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (row.plant_id, row.botanist_id,
                 row.temperature, row.last_watered, row.soil_moisture, row.recording_taken)
            )


if __name__ == "__main__":
    con = get_db_connection()
    all_data = get_all_data()
    upload_to_city_table(con, all_data)
    upload_to_botanist_table(con, all_data)
    upload_to_plant_table(con, all_data)
    upload_to_plant_readings_table(con, all_data)

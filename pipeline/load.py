"""Script to load data to microsoft sql server"""
from os import environ as ENV
from dotenv import load_dotenv
import pyodbc


def get_db_connection() -> pyodbc.Connection:
    """get db connection"""
    load_dotenv()
    conn_str = (f"DRIVER={{{ENV['DB_DRIVER']}}};SERVER={ENV['DB_HOST']};"
                f"PORT={ENV['DB_PORT']};DATABASE={ENV['DB_NAME']};"
                f"UID={ENV['DB_USER']};PWD={ENV['DB_PASSWORD']};Encrypt=no;")

    conn = pyodbc.connect(conn_str)

    return conn


if __name__ == "__main__":
    print(get_db_connection())

import os
from psycopg2 import connect
from dotenv import load_dotenv

load_dotenv()

def connect_to_db():
    """
    Connect to the PostgreSQL database using environment variables.
    Returns:
        connection: A psycopg2 connection object.
    """
    return connect(
        dbname=os.getenv("PG_DATABASE"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST"),
        port=int(os.getenv("PG_PORT"))
    )
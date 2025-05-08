import os
from psycopg2 import connect
from dotenv import load_dotenv
from contextlib import contextmanager

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

@contextmanager
def db_cursor():
    """
    Context manager for database cursor.
    This function creates a connection to the database and yields a cursor.
    It also handles exceptions and ensures that the connection is closed after use.
    """
    conn = connect_to_db()
    cur = conn.cursor()
    try:
        yield cur
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
        raise
    finally:
        cur.close()
        conn.close()
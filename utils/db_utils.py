from contextlib import contextmanager
from db.connection import connect_to_db

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
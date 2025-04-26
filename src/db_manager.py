import psycopg2
import pandas as pd
from db.connection import connect_to_db

def create_table():
    """
    Create table flights in the opensky_flights database.
    """
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        cur.execute("""
            DROP TABLE IF EXISTS flights;
            CREATE TABLE flights (
                icao24 VARCHAR(10) PRIMARY KEY,
                callsign VARCHAR(20),
                origin_country VARCHAR(50),
                time_position TIMESTAMP,
                last_contact TIMESTAMP,
                longitude DOUBLE PRECISION NOT NULL,
                latitude DOUBLE PRECISION NOT NULL,
                baro_altitude DOUBLE PRECISION,
                velocity DOUBLE PRECISION,
                true_track DOUBLE PRECISION,
                vertical_rate DOUBLE PRECISION,
                geo_altitude DOUBLE PRECISION,
                squawk VARCHAR(10),
                spi BOOLEAN
            );
        """)
        conn.commit()
    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def insert_data(df: pd.DataFrame):
    """
    Insert data into the flights table in the opensky_flights database."""
    conn = connect_to_db()
    try:
        cur = conn.cursor()
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO flights 
                (icao24, callsign, origin_country, time_position, last_contact, 
                longitude, latitude, baro_altitude, velocity, true_track, 
                vertical_rate, geo_altitude, squawk, spi) 
                VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (row['icao24'], row['callsign'], row['origin_country'], row['time_position'],
                row['last_contact'], row['longitude'], row['latitude'], row['baro_altitude'],
                row['velocity'], row['true_track'], row['vertical_rate'], row['geo_altitude'],
                row['squawk'], row['spi'])
            )

        conn.commit()

    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


# def select_data(df: pd.DataFrame):
    conn = connect_to_db()
    try:
        cur = conn.cursor()

        # 3. Execute your SQL query - Simple insert
        for _, row in df.iterrows():
            cur.execute(
                "INSERT INTO flights (col1, col2, ...) VALUES (%s, %s, ...)",
                (row[0], row[1], ...)  # Map properly
            )

        # 4. Fetch your results if needed
        rows = cur.fetchall()

        # 5. (Optional) Process your results
        for row in rows:
            print(row)

        # 6. If it was an INSERT/UPDATE/DELETE, commit your changes
        conn.commit()

    except Exception as e:
        print(f"Database error: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()

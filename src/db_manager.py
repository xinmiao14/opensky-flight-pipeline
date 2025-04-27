import psycopg2
import pandas as pd
from utils.db_utils import db_cursor

def create_table():
    """
    Create table flights in the opensky_flights database.
    """
    with db_cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS flights (
                flight_id SERIAL PRIMARY KEY,
                icao24 VARCHAR(10) NOT NULL,
                callsign VARCHAR(20),
                origin_country VARCHAR(50),
                time_position TIMESTAMP,
                last_contact TIMESTAMP,
                longitude DOUBLE PRECISION NOT NULL,
                latitude DOUBLE PRECISION NOT NULL,
                baro_altitude DOUBLE PRECISION,
                ground_speed DOUBLE PRECISION,
                heading DOUBLE PRECISION,
                vertical_rate DOUBLE PRECISION,
                geo_altitude DOUBLE PRECISION,
                squawk VARCHAR(10),
                spi BOOLEAN
            );
        """)
        cur.connection.commit()

def drop_table():
    """
    Drop table flights in the opensky_flights database.
    """
    with db_cursor() as cur:
        cur.execute("""
            DROP TABLE IF EXISTS flights;
        """)
        cur.connection.commit()

def insert_data(df: pd.DataFrame):
    """
    Insert data into the flights table in the opensky_flights database.
    Note: velocity is renamed to ground_speed and true_track to heading
    to match the database schema.
    """
    with db_cursor() as cur:
        for _, row in df.iterrows():
            cur.execute("""
                INSERT INTO flights 
                (icao24, callsign, origin_country, time_position, last_contact, 
                longitude, latitude, baro_altitude, ground_speed, heading, 
                vertical_rate, geo_altitude, squawk, spi) 
                VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
                (row['icao24'], row['callsign'], row['origin_country'], row['time_position'],
                row['last_contact'], row['longitude'], row['latitude'], row['baro_altitude'],
                row['velocity'], row['true_track'], row['vertical_rate'], row['geo_altitude'],
                row['squawk'], row['spi'])
            )
        cur.connection.commit()
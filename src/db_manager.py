import psycopg2
import pandas as pd
from utils.db_utils import db_cursor

def create_table():
    """
    Create table flights in the opensky_flights database.
    Args:
        None
    Returns:
        None
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
    Args:
        None
    Returns:
        None
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
    Args:
        df (pd.DataFrame): DataFrame containing flight data.
    Returns:
        None
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

def get_flight_counts_by_origin_country():
    """
    Query returns the number of flights for each origin country.
    Args:
        None
    Returns:
        list: List of tuples containing origin country and number of flights.
    """
    with db_cursor() as cur:
        cur.execute("""
            SELECT origin_country, COUNT(origin_country) AS number_of_flights 
            FROM flights
            GROUP BY origin_country
            ORDER BY number_of_flights DESC;
        """)
        records = cur.fetchall()
        return records

def get_fastest_and_slowest_ground_speed_by_origin_country():
    """
    Query returns the fastest and slowest ground speed for each origin country.
    Args:
        None
    Returns:
        list: List of tuples containing origin country, max ground speed, and min ground speed.
    """
    with db_cursor() as cur:
        cur.execute("""
            SELECT DISTINCT origin_country, 
                MAX(ground_speed) OVER (PARTITION BY origin_country) AS max_ground_speed,
                MIN(ground_speed) OVER (PARTITION BY origin_country) AS min_ground_speed
            FROM flights
            ORDER BY origin_country;
        """)
        records = cur.fetchall()
        return records
    
def get_average_ground_speed_of_flights_with_and_without_squawk():
    """
    Query returns the average ground speed of flights with and without squawk.
    Args:
        None
    Returns:
        list: List of tuples containing squawk status and average ground speed.
    Note: The squawk status is represented as 'Squawk Present' or 'Squawk Missing'
    """
    with db_cursor() as cur:
        cur.execute("""
            SELECT 'Squawk Present' AS squawk, ROUND(AVG(ground_speed)::NUMERIC, 2) AS average_ground_speed
            FROM flights
            GROUP BY squawk IS NOT NULL
            HAVING squawk IS NOT NULL
            UNION
            SELECT 'Squawk Missing' AS squawk, ROUND(AVG(ground_speed)::NUMERIC, 2) AS average_ground_speed
            FROM flights
            GROUP BY squawk
            HAVING squawk IS NULL;
        """)
        records = cur.fetchall()
        return records
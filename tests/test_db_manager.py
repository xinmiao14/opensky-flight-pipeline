import pytest
from decimal import Decimal
from src.fetch import get_flight_data
from src.transform import clean_data
from src.load import load_data
from src.db_manager import (create_table, drop_table, insert_data, get_flight_counts_by_origin_country,
                            get_fastest_and_slowest_ground_speed_by_origin_country,
                            get_average_ground_speed_of_flights_with_and_without_squawk)
from utils.db_utils import db_cursor

@pytest.fixture(scope="module")
def raw_data():
    """Fixture to fetch flight data."""
    return get_flight_data()

@pytest.fixture(scope="module")
def cleaned_data(raw_data):
    """Fixture to clean flight data."""
    return clean_data(raw_data[0], raw_data[1])

@pytest.fixture(scope="module")
def loaded_data(cleaned_data):
    """Fixture to load cleaned flight data."""
    return load_data(cleaned_data[0], cleaned_data[1])

@pytest.fixture(scope="module")
def database_setup(loaded_data):
    """Fixture to set up the database."""
    drop_table()
    create_table()
    insert_data(loaded_data)

class TestCreateTable:
    def test_table_flights_exists(self):
        with db_cursor() as cur:
            create_table()
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'flights');
                """)
            exists = cur.fetchone()[0]
        assert exists is True

    def test_table_flights_has_correct_columns(self):
        with db_cursor() as cur:
            create_table()
            cur.execute("""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = 'flights'
                ORDER BY ordinal_position;
            """)
            columns = [row[0] for row in cur.fetchall()]

        expected_columns = ["flight_id", "icao24", "callsign", "origin_country", 
                            "time_position", "last_contact", "longitude", "latitude", 
                            "baro_altitude", "ground_speed", "heading", "vertical_rate", 
                            "geo_altitude", "squawk", "spi"]
        assert columns == expected_columns

class TestDropTable:
    def test_table_flights_does_not_exist(self):
        with db_cursor() as cur:
            drop_table()
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'flights');
                """)
            exists = cur.fetchone()[0]
        assert exists is False

class TestInsertData:
    def test_table_flights_is_not_empty(self, database_setup):
        with db_cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) FROM flights;
            """)
            record_count = cur.fetchone()[0]
        assert record_count > 0

    def test_table_flights_has_correct_number_of_records(self, loaded_data, database_setup):
        with db_cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) FROM flights;
            """)
            record_count = cur.fetchone()[0]
        assert record_count == len(loaded_data)

class TestGetFlightCountsByOriginCountry:
    def test_query_returns_a_non_empty_result(self, database_setup):
        length = len(get_flight_counts_by_origin_country())
        assert length > 0
    
    def test_query_returns_a_list_of_tuples(self, database_setup):
        result = get_flight_counts_by_origin_country()
        assert isinstance(result, list)
        assert all(isinstance(item, tuple) for item in result)
    
    def test_query_returns_correct_number_of_columns(self, database_setup):
        result = get_flight_counts_by_origin_country()
        assert len(result[0]) == 2

    def test_query_returns_correct_datatypes_for_each_column(self, database_setup):
        result = get_flight_counts_by_origin_country()
        assert all(isinstance(item[0], str) for item in result)  # origin_country
        assert all(isinstance(item[1], int) for item in result)

class TestGetFastestAndSlowestGroundSpeedByOriginCountry:
    def test_query_returns_a_non_empty_result(self, database_setup):
        length = len(get_fastest_and_slowest_ground_speed_by_origin_country())
        assert length > 0
    
    def test_query_returns_a_list_of_tuples(self, database_setup):
        result = get_fastest_and_slowest_ground_speed_by_origin_country()
        assert isinstance(result, list)
        assert all(isinstance(item, tuple) for item in result)
    
    def test_query_returns_correct_number_of_columns(self, database_setup):
        result = get_fastest_and_slowest_ground_speed_by_origin_country()
        assert len(result[0]) == 3

    def test_query_returns_correct_datatypes_for_each_column(self, database_setup):
        result = get_fastest_and_slowest_ground_speed_by_origin_country()
        assert all(isinstance(item[0], str) for item in result)
        assert all(isinstance(item[1], float) for item in result)
        assert all(isinstance(item[2], float) for item in result)

class TestGetAverageGroundSpeedOfFlightsWithAndWithoutSquawk:
    def test_query_returns_a_non_empty_result(self, database_setup):
        length = len(get_average_ground_speed_of_flights_with_and_without_squawk())
        assert length > 0
    
    def test_query_returns_a_list_of_tuples(self, database_setup):
        result = get_average_ground_speed_of_flights_with_and_without_squawk()
        assert isinstance(result, list)
        assert all(isinstance(item, tuple) for item in result)
    
    def test_query_returns_correct_number_of_columns(self, database_setup):
        result = get_average_ground_speed_of_flights_with_and_without_squawk()
        assert len(result[0]) == 2

    def test_query_returns_correct_datatypes_for_each_column(self, database_setup):
        result = get_average_ground_speed_of_flights_with_and_without_squawk()
        assert all(isinstance(item[0], str) for item in result)
        assert all(isinstance(item[1], Decimal) for item in result)
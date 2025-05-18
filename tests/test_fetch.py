import os
import pytest
from src.fetch import get_flight_data

@pytest.fixture(scope="module")
def flight_data():
    """Fixture to fetch flight data."""
    return get_flight_data()

raw_flight_data_json_file_path = "data/raw_flight_data.json"
raw_flight_data_csv_file_path = "data/raw_flight_data.csv"

class TestGetFlightData:
    def test_get_flight_data_returns_a_tuple_containing_flight_data_and_timestamp(self, flight_data):
        assert isinstance(flight_data, tuple)
        assert len(flight_data) == 2

    def test_get_flight_data_returns_raw_flight_data_as_a_dict(self, flight_data):
        assert isinstance(flight_data[0], dict)

    def test_raw_data_has_states_key(self, flight_data):
        assert "states" in flight_data[0]

    def test_raw_data_states_has_a_non_empty_list(self, flight_data):
        assert isinstance(flight_data[0]["states"], list)
        assert len(flight_data[0]["states"]) > 0
    
    def test_raw_data_returns_flight_data_in_lists(self, flight_data):
        assert isinstance(flight_data[0]["states"][0], list)
        assert len(flight_data[0]["states"][0]) > 0
    
    def test_utc_timestamp_is_correct_format(self, flight_data):
        assert isinstance(flight_data[1], str)

class TestGetFlightDataFile:
    def test_raw_flight_data_json_file_exists(self):
        assert os.path.exists(raw_flight_data_json_file_path)

    def test_raw_flight_data_file_is_not_empty(self):
        assert os.path.getsize(raw_flight_data_json_file_path) > 0

    def test_raw_flight_data_csv_file_exists(self):
        assert os.path.exists(raw_flight_data_csv_file_path)

    def test_raw_flight_data_csv_file_is_not_empty(self):
        assert os.path.getsize(raw_flight_data_csv_file_path) > 0
import os
import pytest
from src.fetch import get_flight_data

@pytest.fixture(scope="module")
def flight_data():
    """Fixture to fetch flight data."""
    return get_flight_data()

raw_flight_data_file_path = "data/raw_flight_data.json"

class TestGetFlightData:
    def test_get_flight_data_returns_a_dictionary(self, flight_data):
        assert isinstance(flight_data, dict)

    def test_get_flight_data_has_states_key(self, flight_data):
        assert "states" in flight_data

    def test_get_flight_data_states_has_a_non_empty_list(self, flight_data):
        assert isinstance(flight_data["states"], list)
        assert len(flight_data["states"]) > 0
    
    def test_get_flight_data_returns_flight_data_in_lists(self, flight_data):
        assert isinstance(flight_data["states"][0], list)
        assert len(flight_data["states"][0]) > 0

class TestGetFlightDataFile:
    def test_raw_flight_data_file_exists(self):
        assert os.path.exists(raw_flight_data_file_path)

    def test_raw_flight_data_file_is_not_empty(self):
        assert os.path.getsize(raw_flight_data_file_path) > 0
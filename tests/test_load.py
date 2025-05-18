import os
import pandas as pd
import pytest
from src.fetch import get_flight_data
from src.transform import clean_data
from src.load import load_data

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

@pytest.mark.parametrize("file_path", [
                        os.path.join("data", "cleaned_flight_data.csv"),
                        os.path.join("data", "cleaned_flight_data.jsonl")
                        ])
class TestLoadData:
    def test_load_data_export_to_csv_and_json(self, file_path):
        assert os.path.exists(file_path)

    def test_cleaned_flight_data_csv_and_json_not_empty(self, file_path):
        assert os.path.getsize(file_path) > 0


class TestLoadDataDataFrame:
    def test_load_data_returns_a_dataframe(self, loaded_data):
        assert isinstance(loaded_data, pd.DataFrame)

    def test_load_data_dataframe_not_empty(self, loaded_data):
        assert not loaded_data.empty
        assert len(loaded_data) > 0

    def test_load_data_dataframe_has_14_columns(self, loaded_data):
        assert loaded_data.shape[1] == 14
    
    def test_load_data_dataframe_columns(self, loaded_data):
        expected_columns = ["icao24", "callsign", "origin_country", "time_position", 
                            "last_contact", "longitude", "latitude", "baro_altitude", 
                            "velocity", "true_track", "vertical_rate", "geo_altitude", 
                            "squawk", "spi"]
        assert list(loaded_data.columns) == expected_columns

    def test_loaded_data_dataframe_contains_flight_data(self, loaded_data):
        assert loaded_data.shape[0] > 0
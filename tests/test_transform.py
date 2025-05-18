import pandas as pd
import pytest
from src.fetch import get_flight_data
from src.transform  import clean_data

@pytest.fixture(scope="module")
def raw_data():
    """Fixture to fetch flight data."""
    return get_flight_data()

@pytest.fixture(scope="module")
def cleaned_data(raw_data):
    """Fixture to clean flight data."""
    return clean_data(raw_data[0], raw_data[1])

class TestCleanData:
    def test_clean_data_returns_a_tuple_of_length_2(self, cleaned_data):
        assert isinstance(cleaned_data, tuple)
        assert len(cleaned_data) == 2

    def test_clean_data_returns_a_tuple_containing_a_dataframe_and_timestamp(self, cleaned_data):
        assert isinstance(cleaned_data[0], pd.DataFrame)
        assert isinstance(cleaned_data[1], str)

    def test_clean_data_dataframe_is_not_empty(self, cleaned_data):
        assert not cleaned_data[0].empty
        assert len(cleaned_data[0]) > 0
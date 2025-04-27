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
    return clean_data(raw_data)

class TestCleanData:
    def test_clean_data_returns_a_dataframe(self, cleaned_data):
        assert isinstance(cleaned_data, pd.DataFrame)

    def test_clean_data_dataframe_not_empty(self, cleaned_data):
        assert not cleaned_data.empty
        assert len(cleaned_data) > 0
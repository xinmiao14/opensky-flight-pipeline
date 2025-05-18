import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    return TestClient(app)

class TestRootEndpoint:
    def test_root_endpoint_returns_welcome_message(self, client):
        endpoint = "/"
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.json() == {"message": "🛫 Welcome to OpenSky Flight Data Pipeline"}

class TestHealthcheckEndpoint:
    def test_healthcheck_endpoint_returns_ok(self, client):
        endpoint = "/healthcheck"
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.json() == {"status": "OK"}

class TestFetchFlightsEndpoint:
    def test_fetch_flights_endpoint_returns_number_of_records_inserted(self, client):
        endpoint = "/fetch-flights"
        response = client.get(endpoint)
        assert response.status_code == 200
        assert response.json()["status"] == "success"
        assert response.json()["records_inserted"] > 0

    @pytest.mark.skip(reason="Cannot reliably simulate fetch-flights error without mocking")
    def test_fetch_flights_endpoint_returns_error_on_failure(self, client):
        endpoint = "/fetch-flights"
        response = client.get(endpoint)
        assert response.status_code == 500
        assert "detail" in response.json()

class TestFlightCountsByOriginCountryEndpoint:
    def test_flight_counts_by_origin_country_endpoint_returns_counts(self, client):
        endpoint = "/flight-counts-by-origin-country"
        response = client.get(endpoint)
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        query_data = body["data"]
        assert len(query_data) > 0
        assert all(isinstance(item, list) for item in query_data)
        assert all(len(item) == 2 for item in query_data)
        assert all(isinstance(item[0], str) and isinstance(item[1], int) for item in query_data)

class TestGetFastestAndSlowestGroundSpeedByOriginCountry:
    def test_query_returns_the_fastest_and_slowest_ground_speed_for_each_country(self, client):
        endpoint = "/fastest-and-slowest-ground-speed-by-origin-country"
        response = client.get(endpoint)
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        query_data = body["data"]
        assert len(query_data) > 0
        assert all(isinstance(item, list) for item in query_data)
        assert all(len(item) == 3 for item in query_data)
        assert all(isinstance(item[0], str) 
                    and isinstance(item[1], float) 
                    and isinstance(item[2], float) for item in query_data)
        assert all(item[1] >= item[2] for item in query_data)

class TestGetAverageGroundSpeedOfFlightsWithAndWithoutSquawk:
    def test_query_returns_the_average_ground_speed_of_flights_with_and_without_squawk(self, client):
        endpoint = "/average-ground-speed-of-flights-with-and-without-squawk"
        response = client.get(endpoint)
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "success"
        query_data = body["data"]
        assert len(query_data) == 2
        assert all(isinstance(item, list) for item in query_data)
        assert all(len(item) == 2 for item in query_data)
        assert query_data[0][0] == "Squawk Present" or query_data[0][0] == "Squawk Missing"
        assert query_data[1][0] == "Squawk Missing" or query_data[1][0] == "Squawk Present"
        assert query_data[0][0] != query_data[1][0]
        assert isinstance(query_data[0][1], float) and isinstance(query_data[1][1], float)
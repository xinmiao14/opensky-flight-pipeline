import requests
import json

def get_flight_data():
    """
    Fetches flight data from the OpenSky Network API.
    Returns:
        dict: A dictionary containing flight data.
    """
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url)
    response.raise_for_status()

    with open('data/raw_flight_data.json', 'w', encoding='utf-8') as json_file:
        json.dump(response.json(), json_file, indent=4)

    return response.json()
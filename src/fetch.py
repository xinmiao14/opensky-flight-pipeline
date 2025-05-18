import requests
import json
import csv
import boto3
import os
import datetime

def get_flight_data():
    """
    Fetches flight data from the OpenSky Network API. The data is saved in both JSON 
    and CSV formats in the 'data' directory. The JSON and CSV files are then uploaded 
    to an S3 bucket. A timestamp is used to create a unique folder structure in the 
    S3 bucket.
    Args:
        None
    Returns:
        tuple: A tuple containing the raw flight data as a dictionary and the UTC 
               timestamp of the data retrieval as a string.
    """
    # Fetch flight data from OpenSky Network API
    url = "https://opensky-network.org/api/states/all"
    response = requests.get(url)
    response.raise_for_status()
    raw_data = response.json()

    os.makedirs("data", exist_ok=True)  # This creates /app/data inside the container
    
    # Save the raw data to JSON and CSV files
    file_path_json = os.path.join("data", "raw_flight_data.json")
    with open(file_path_json, 'w', encoding='utf-8') as json_file:
        json.dump(raw_data, json_file, indent=4)
    
    file_path_csv = os.path.join("data", "raw_flight_data.csv")
    with open(file_path_csv, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write header
        writer.writerow([
            "icao24", "callsign", "origin_country", "time_position", 
            "last_contact", "longitude", "latitude", "baro_altitude", 
            "on_ground", "velocity", "true_track", "vertical_rate", 
            "sensors", "geo_altitude", "squawk", "spi", "position_source"
    ])
        # Write data rows
        for flight in raw_data.get('states', []):
            writer.writerow(flight[:17])  # ensures exactly 17 columns are written

    # Upload the files to S3
    s3  = boto3.client("s3")
    bucket_name = os.getenv("S3_DATA_BUCKET", "opensky-data-bucket")
    
    timestamp = raw_data["time"]
    # Convert the timestamp to ISO format
    utc_timestamp = datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).strftime('%Y-%m-%d_%H-%M-%S')
    s3.upload_file(
        Filename = file_path_json,
        Bucket = bucket_name,
        # Use the UTC timestamp to create a unique folder structure
        Key = f"data/{utc_timestamp}/raw_flight_data.json"
    )
    s3.upload_file(
        Filename = file_path_csv,
        Bucket = bucket_name,
        Key = f"data/{utc_timestamp}/raw_flight_data.csv"
    )

    return (raw_data, utc_timestamp)
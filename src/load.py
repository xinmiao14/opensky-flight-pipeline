import os
import pandas as pd
import boto3

def load_data(cleaned_data, timestamp):
    """
    Load selected columns of cleaned flight data into CSV and JSON files, and upload to S3.
    Args:
        cleaned_data (pd.DataFrame): Cleaned flight data.
        timestamp (str): UTC timestamp of the data retrieval.
    Returns:
        pd.DataFrame: DataFrame containing the cleaned flight data.
    """
    # Columns removed: "on_ground" - all False, "sensors" - data not available, "position_source" - all data from ADS-B
    columns_to_export = ["icao24", "callsign", "origin_country", "time_position", 
                        "last_contact", "longitude", "latitude", "baro_altitude", 
                        "velocity", "true_track", "vertical_rate", "geo_altitude", 
                        "squawk", "spi"]
    df_selected = cleaned_data[columns_to_export]

    # Ensure the DataFrame is not empty before saving
    if df_selected.empty:
        raise ValueError("No data available to load.")
    
    file_path_csv = os.path.join("data", "cleaned_flight_data.csv")
    file_path_jsonl = os.path.join("data", "cleaned_flight_data.jsonl")
    df_selected.to_csv(file_path_csv, index=False)
    df_selected.to_json(file_path_jsonl, orient="records", date_format="iso", lines=True)

    # Upload the files to S3 bucket
    bucket_name = os.getenv("S3_DATA_BUCKET", "opensky-dev-data")
    s3 = boto3.client("s3")
    s3.upload_file(
        Filename = file_path_jsonl,
        Bucket = bucket_name,
        Key = f"data/{timestamp}/cleaned_flight_data.jsonl"
    )
    s3.upload_file(
        Filename = file_path_csv,
        Bucket = bucket_name,
        Key = f"data/{timestamp}/cleaned_flight_data.csv"
    )
    
    return df_selected
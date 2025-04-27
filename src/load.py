import pandas as pd

def load_data(cleaned_data):
    """
    Save selected columns of cleaned flight data to files and return the filtered DataFrame.
    """
    # Columns removed: "on_ground" - all False, "sensors" - data not available, "position_source" - all data from ADS-B
    columns_to_export = ["icao24", "callsign", "origin_country", "time_position", 
                        "last_contact", "longitude", "latitude", "baro_altitude", 
                        "velocity", "true_track", "vertical_rate", "geo_altitude", 
                        "squawk", "spi"]
    df_selected = cleaned_data[columns_to_export]

    if df_selected.empty:
        raise ValueError("No data available to load.")
    
    df_selected.to_csv("data/cleaned_flight_data.csv", index=False)
    df_selected.to_json("data/cleaned_flight_data.json", orient="records", date_format="iso", lines=True)
    
    return df_selected
import pandas as pd

def clean_data(raw_data):
    """
    Clean and transform the raw flight data from OpenSky API.
    Args:
        raw_data: Raw flight data from OpenSky API.
    Returns:
        pd.DataFrame: Cleaned flight data.
    """
    flight_data = raw_data.get("states", [])

    # Columns from OpenSky documentation: https://openskynetwork.github.io/opensky-api/rest.html
    columns = ["icao24", "callsign", "origin_country", "time_position", 
                "last_contact", "longitude", "latitude", "baro_altitude", 
                "on_ground", "velocity", "true_track", "vertical_rate", 
                "sensors", "geo_altitude", "squawk", "spi", "position_source"]
    df = pd.DataFrame(flight_data, columns = columns)
    
    # Replace missing callsigns with "UNKNOWN"
    df["callsign"] = df["callsign"].fillna("UNKNOWN")

    # Ensure callsigns are strings and replace missing values with "UNKNOWN" 
    df["callsign"] = df["callsign"].astype(str).str.strip()
    df["callsign"] = df["callsign"].replace({"nan": "UNKNOWN", "": "UNKNOWN"})

    # Replace missing squawk with None
    df["squawk"] = df["squawk"].where(pd.notna(df["squawk"]), None)

    # Drop rows where essential data is missing (longitude, latitude)
    df = df.dropna(subset = ["longitude", "latitude"])

    # Convert velocity & altitude fields to numeric
    df["velocity"] = pd.to_numeric(df["velocity"], errors="coerce").where(pd.notna(df["velocity"]), None)
    df["baro_altitude"] = pd.to_numeric(df["baro_altitude"], errors="coerce").where(pd.notna(df["baro_altitude"]), None)
    df["geo_altitude"] = pd.to_numeric(df["geo_altitude"], errors="coerce").where(pd.notna(df["geo_altitude"]), None)

    # Convert Unix timestamp to Datetime format
    df["time_position"] = pd.to_datetime(df["time_position"], unit="s")
    df["last_contact"] = pd.to_datetime(df["last_contact"], unit="s")

    # Convert velocity unit from m/s to knots
    df["velocity"] = round(df["velocity"] * 1.944, 4)
    # Convert vertical_rate unit from m/s to feet/min
    df["vertical_rate"] = round(df["vertical_rate"] * 196.850, 4)

    # Convert altitude units from metres to feet
    df["baro_altitude"] = round(df["baro_altitude"] * 3.281, 4)
    df["geo_altitude"] = round(df["geo_altitude"] * 3.281, 4)

    # Filter out flights that are on the ground (we want airborne flights only)
    df = df[df["on_ground"] == False]

    # Remove flights with extremely low speeds (potential stationary aircraft)
    # ICAO maximum taxi speed is 30 knots (15.43m/s)
    df = df[df["velocity"] > 16]

    # Remove flights with invalid callsigns (just 'UNKNOWN' or empty)
    df = df[df["callsign"] != "UNKNOWN"]

    return df
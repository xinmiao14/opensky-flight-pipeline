from fastapi import FastAPI, HTTPException
from src.fetch import get_flight_data
from src.transform import clean_data
from src.load import load_data
from src.db_manager import (
    create_table, drop_table, insert_data, 
    get_flight_counts_by_origin_country,
    get_fastest_and_slowest_ground_speed_by_origin_country,
    get_average_ground_speed_of_flights_with_and_without_squawk
    )

app = FastAPI()

@app.get("/")
def root():
    return {"message": "🛫 Welcome to OpenSky Flight Data Pipeline"}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "OK"}

@app.get("/fetch-flights")
def fetch_flights():
    """
    Fetch flight data from OpenSky API, clean it, and load it into the database.
    """
    try:
        data = get_flight_data()
        cleaned_data = clean_data(data)
        loaded_data = load_data(cleaned_data)
        drop_table()
        create_table()
        insert_data(loaded_data)
        return {"status": "success", "records_inserted": len(loaded_data)}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
@app.get("/flight-counts-by-origin-country")
def flight_counts_by_origin_country():
    """
    Get flight counts by origin country.
    """
    try:
        counts = get_flight_counts_by_origin_country()
        return {"status": "success", "data": counts}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
@app.get("/fastest-and-slowest-ground-speed-by-origin-country")
def fastest_and_slowest_ground_speed_by_origin_country():
    """
    Get the fastest and slowest ground speed for each origin country.
    """
    try:
        speeds = get_fastest_and_slowest_ground_speed_by_origin_country()
        return {"status": "success", "data": speeds}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
    
@app.get("/average-ground-speed-of-flights-with-and-without-squawk")
def average_ground_speed_of_flights_with_and_without_squawk():
    """
    Get the average ground speed of flights with and without squawk.
    """
    try:
        speeds = get_average_ground_speed_of_flights_with_and_without_squawk()
        return {"status": "success", "data": speeds}
    except Exception as e:
        raise HTTPException(status_code = 500, detail = str(e))
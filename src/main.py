from fastapi import FastAPI
from src.fetch import get_flight_data
from src.transform import clean_data
from src.db_manager import create_table, insert_data

app = FastAPI()

@app.get("/")
def root():
    return {"message": "🛫 Welcome to OpenSky Flight Data Pipeline"}

@app.get("/healthcheck")
def healthcheck():
    return {"status": "OK"}

@app.get("/fetch-flights")
def fetch_flights():
    try:
        data = get_flight_data()
        cleaned_data = clean_data(data)
        create_table()
        insert_data(cleaned_data)
        return {"status": "success", "records": len(cleaned_data)}
    except Exception as e:
        return {"status": "error", "details": str(e)}
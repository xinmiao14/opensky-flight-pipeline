# OpenSky Flight Data Pipeline

## Overview
This project fetches live flight telemetry data from the OpenSky Network API, processes and cleans it using Python, and stores structured flight information in a PostgreSQL database. It also exposes a FastAPI-based API to trigger data ingestion and monitor status.

## Features
- FastAPI server with `/fetch-flights` endpoint
- Real-time data fetching from OpenSky Network
- Data cleaning and validation using pandas
- PostgreSQL storage with psycopg2-binary
- Unit and integration tests planned with pytest

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- Pandas
- psycopg2-binary
- Uvicorn
- Pytest

## Setup Instructions
1. Clone the repo
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Start PostgreSQL locally and create a database.
5. Run the API server:
    ```bash
    uvicorn src.main:app --reload
    ```

## Project Structure
data/
cleaned_flight_data.json
cleaned_flight_data.csv
raw_flight_data.json
db/
connection.py
db_setup.sql
src/
main.py
fetch.py
transform.py
db_manager.py
tests/
test_fetch.py
test_transform.py
test_db_manager.py

## Future Improvements
- Dockerise the application
- Deploy on AWS EC2 + RDS
- Set up GitHub Actions for automated tests
- Add data validation with pydantic
- Build simple dashboards for live data monitoring
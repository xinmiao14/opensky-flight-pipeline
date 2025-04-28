# OpenSky Flight Data Pipeline

# Highlights
- 🛰️ **Live Flight Fetching:** Fetches real-time flight telemetry from OpenSky API
- 🧹 **Data Cleaning:** Transforms and validates flight records using pandas
- 🗄️ **PostgreSQL Storage:** Stores structured flight data in a relational database
- ⚡ **FastAPI Endpoints:** Provides clean API access for analytics
- 🛡️ **Resilient Structure:** Designed to handle API rate limits and real-world instability
- 🛠️ **Modular Architecture:** Clear separation of fetch, clean, load, and serve
- ✈️ **Next Steps:** Dockerisation, AWS deployment, CI/CD integration

## Overview
This project fetches live flight telemetry data from the OpenSky Network API, processes and cleans it using Python, and stores structured flight information in a PostgreSQL database. It exposes a FastAPI-based API to trigger data ingestion and run analytic queries.

## Features
- FastAPI server with multiple endpoints:
  - `/fetch-flights`: Fetch and ingest fresh flight data
  - `/flight-counts-by-origin-country`: Query flight counts grouped by origin country
  - `/fastest-and-slowest-ground-speed-by-origin-country`: Query fastest and slowest ground speeds by origin country
  - `/average-ground-speed-of-flights-with-and-without-squawk`: Compare average speeds based on squawk presence
- Real-time data fetching from OpenSky Network
- Data cleaning and validation using pandas
- PostgreSQL storage with psycopg2-binary
- Full unit and integration tests using pytest
- Modular codebase separating fetching, cleaning, loading, and database management

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- Pandas
- psycopg2-binary
- Uvicorn
- Pytest

## Setup Instructions
1. Clone the repo:
    ```bash
    git clone https://github.com/xinmiao14/opensky-flight-data-pipeline.git
    cd opensky-flight-data-pipeline
    ```
2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Start PostgreSQL locally and create a database:
    ```bash
    CREATE DATABASE opensky_flights;
    ```
5. Run the API server locally:
    ```bash
    uvicorn src.main:app --reload
    ```
    
## Project Structure
```
data/
  cleaned_flight_data.csv
  cleaned_flight_data.json
  raw_flight_data.json

db/
  connection.py
  db_setup.sql

utils/
  db_utils.py

src/
  main.py
  fetch.py
  transform.py
  load.py
  db_manager.py

tests/
  test_fetch.py
  test_transform.py
  test_load.py
  test_db_manager.py
  test_main.py
```

## Future Improvements
- Dockerise the application
- Deploy backend on AWS EC2 + database on AWS RDS
- Set up GitHub Actions for CI/CD and automated testing
- Add schema validation with pydantic
- Implement retry and backoff strategies for API stability
- Build a simple dashboard for live flight monitoring
# OpenSky Flight Data Pipeline

## Highlights
- 🛰️ **Live Flight Fetching:** Fetches real-time flight telemetry from OpenSky API
- 🧹 **Data Cleaning:** Validates and transforms flight records using pandas
- 🗄️ **PostgreSQL Storage:** Stores structured flight data in a relational database
- ⚡ **FastAPI Endpoints:** Provides clean API access for analytics
- 🛡️ **Resilient Structure:** Designed to handle API rate limits and real-world instability
- 🛠️ **Modular Architecture:** Clear separation of fetch, clean, load, and serve
- ✈️ **Next Steps:** CI/CD integration, retries with exponential backoff

## Overview
This project fetches live flight telemetry data from the OpenSky Network API, processes and cleans it using Python, and stores structured flight information in a PostgreSQL database. It exposes a FastAPI-based API to trigger data ingestion and run analytic queries.

## Features
- FastAPI server with the following endpoints:
  - `/fetch-flights`: Fetch and ingest fresh flight data
  - `/flight-counts-by-origin-country`: Query flight counts grouped by origin country
  - `/fastest-and-slowest-ground-speed-by-origin-country`: Query fastest and slowest ground speeds by origin country
  - `/average-ground-speed-of-flights-with-and-without-squawk`: Compare average speeds based on squawk presence
- Real-time data fetching from OpenSky Network
- Data cleaning with pandas
- PostgreSQL storage with psycopg2
- Full unit and integration tests using pytest
- Modular codebase separating fetching, cleaning, loading, and database management
- Containerised with Docker
- Cloud-deployable via Terraform

## Tech Stack
- Python
- FastAPI
- PostgreSQL
- Pandas
- psycopg2-binary
- Uvicorn
- Pytest
- Docker
- Terraform

## Setup Instructions

This project can be run in three ways:

### ▶️ Local Python environment
1. **Clone the repo:**
    ```bash
    git clone https://github.com/xinmiao14/opensky-flight-data-pipeline.git
    cd opensky-flight-data-pipeline
    ```
2. **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4. **Start PostgreSQL locally and create a database:**
    ```bash
    CREATE DATABASE opensky_flights;
    ```
5. **Run the API server locally:**
    ```bash
    uvicorn src.main:app --reload
    ```

### 🐳 Docker Deployment (Local)
1. **Build the Docker image:**
    ```bash
    docker build -t opensky-app -f docker/Dockerfile.api .
    ```

2. **Run the container:**
    ```bash
    docker compose up
    ```
> Ensure your `docker-compose.yml` file is present in the project root

### ☁️ AWS Deployment (Terraform)
You can deploy the full stack to AWS using Terraform:
1. **Bootstrap the remote Terraform backend:**
    ```bash
    cd terraform-bootstrap
    terraform init
    terraform plan
    terraform apply
    ```

2. **Deploy the full infrastructure:**
    ```bash
    cd ../terraform
    terraform init
    terraform plan
    terraform apply
    ```

3. **SSH into the EC2 instance and run your container:**
    ```bash
    ssh -i your-key.pem ec2-user@<public-ip>
    docker pull xinmiao14/opensky-app
    docker compose up
    ```
> Ensure your `.env` and `docker-compose.yml` files are present on the EC2 instance with the correct S3 and PostgreSQL environment variables.

## Project Structure
```
data/
  cleaned_flight_data.csv
  cleaned_flight_data.jsonl
  raw_flight_data.csv
  raw_flight_data.json

db/
  db_setup.sql

docker/
  docker-entrypoint.sh
  Dockerfile.api

src/
  main.py
  fetch.py
  transform.py
  load.py
  db_manager.py

terraform/
  iam.tf
  main.tf
  outputs.tf
  provider.tf
  variables.tf

terraform-bootstrap/
  main.tf

tests/
  test_fetch.py
  test_transform.py
  test_load.py
  test_db_manager.py
  test_main.py

utils/
  db_utils.py
```

## Future Improvements
- CI/CD with GitHub Actions
- Schema validation with pydantic
- Retry/backoff logic for external APIs
- Automated ingestion (e.g. every 15 minutes)
- Lightweight dashboard for live flight insights
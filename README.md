# FuelSenseAI

FuelSenseAI is a Flask-based web application that recommends nearby fuel stations using geographic search, weather-aware crowd prediction, and user feedback.

## Features

- Search for locations using Geoapify geocoding
- Discover nearby fuel stations using Geoapify places API
- Predict waiting times and station crowd based on weather and historical patterns
- Save user feedback for predicted and actual wait times
- Deploy locally with Docker or on cloud platforms using `Procfile`

## Requirements

- Python 3.11+ (or 3.12+ recommended)
- `pip` package manager
- A valid Geoapify API key
- Docker (optional)

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yashraj-shishodia/FuelSenseAI.git
cd FuelSenseAI
```

2. Install Python dependencies:
```bash
python3 -m pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```env
GEOAPIFY_API_KEY=your_real_key_here
```

4. Run the application locally:
```bash
python3 app.py
```

The application will run at `http://127.0.0.1:5000`.

## Docker

Build the Docker image:
```bash
docker build -t fuelsenseai .
```

Run the container with your Geoapify key:
```bash
docker run -p 5001:5000 -e GEOAPIFY_API_KEY=your_real_key_here fuelsenseai
```

Then open `http://127.0.0.1:5001`.

## Deployment

This project includes a `Dockerfile` and `Procfile` for deployment. Use your cloud provider of choice and set `GEOAPIFY_API_KEY` as an environment variable.

## Project Structure

- `app.py` — Flask application entrypoint
- `api/` — API wrappers for geocoding, station lookup, weather, and prediction
- `database/` — SQLite helpers for prediction history and feedback
- `static/` — frontend JavaScript, CSS, and assets
- `templates/` — HTML templates
- `Dockerfile`, `Procfile`, `.dockerignore` — deployment configuration

## Notes

- Do not commit `.env` or your API key
- Keep API keys secret
- The repo excludes large models and datasets to keep it lightweight

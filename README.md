# FuelSenseAI

FuelSenseAI is a Flask-based web application that recommends nearby fuel stations using geographic search, weather-aware crowd prediction, and user feedback.

## Features

- Search for locations using Geoapify geocoding
- Discover nearby fuel stations using Geoapify places API
- Predict waiting times and station crowd based on weather and historical patterns
- Save user feedback for predicted and actual wait times
- Run locally with Python or deploy on cloud platforms using `Procfile`

## Requirements

- Python 3.11+ (or 3.12+ recommended)
- `pip` package manager
- A valid Geoapify API key
- `pip` package manager

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

## Deployment

This project supports local Python execution and cloud deployment using `Procfile`.

Set `GEOAPIFY_API_KEY` in your cloud provider's environment variables.

### Vercel

To deploy on Vercel without Docker, use a serverless or custom deployment configuration and set the environment variable:

```bash
GEOAPIFY_API_KEY=your_real_key_here
```

### Other providers

Use the existing `Procfile` or your preferred Python deployment workflow.

- Run locally:

```bash
python3 app.py
```

## Project Structure

### Vercel

This project can be deployed to Vercel using the included `Dockerfile` and `vercel.json` configuration. Create a new Vercel project from this repository, then set the environment variable:

```bash
GEOAPIFY_API_KEY=your_real_key_here
```

The Dockerfile uses the `PORT` environment variable so Vercel can route traffic correctly.

### Other providers

This project also supports Docker-based deployment and Heroku-style deployment.

- For Docker:

```bash
docker build -t fuelsenseai .
docker run -p 5001:5000 -e GEOAPIFY_API_KEY=your_real_key_here fuelsenseai
```

- For cloud providers with `Procfile`, use the existing `Procfile`.

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

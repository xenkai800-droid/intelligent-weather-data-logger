# Intelligent Weather Data Logger

A Streamlit dashboard that retrieves current weather from Open-Meteo and turns it into comfort scores, risk assessments, recommendations, and an ML comfort prediction. Historical observations can be stored locally in SQLite and explored through interactive charts.

## Features

- Fetch current conditions for six Indian cities using the free Open-Meteo API.
- Calculate weather comfort, heat stress, dehydration, and outdoor activity risks.
- Show hydration, clothing, and activity recommendations.
- Predict a comfort category with the included trained model.
- Store observations in a local SQLite database and visualize historical data.

## Requirements

- Python 3.11 or newer
- Internet access to retrieve live weather

## Run locally

```bash
git clone https://github.com/xenkai800-droid/intelligent-weather-data-logger.git
cd intelligent-weather-data-logger
python -m venv .venv
```

Activate the environment, then install and start the dashboard:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app/dashboard.py
```

Streamlit prints a local URL after startup. The app creates `data/weather.db` and the required tables automatically. The database and logs stay local and are excluded from Git. Historical charts populate as weather observations are collected.

## Project layout

- `app/`: Streamlit dashboard
- `api/`: Open-Meteo current and historical weather clients
- `analytics/`: Comfort, anomaly, risk, and recommendation logic
- `database/`: SQLite schema and data access
- `ml/`: Trained model artifacts, training, and prediction code
- `scripts/`: Historical data import and training-data preparation
- `visualizations/`: Historical weather charts
- `tests/`: Unit tests

## Data source

Live and historical weather data are retrieved from [Open-Meteo](https://open-meteo.com/). No API key is required.

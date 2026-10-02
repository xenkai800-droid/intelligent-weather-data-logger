# Project Structure

```text
.
├── analytics/             Comfort, anomaly, risk, and recommendation rules
├── api/                   Open-Meteo current and archive clients
├── app/                   Streamlit dashboard
├── config/                YAML configuration and settings loader
├── database/              SQLite schema and database access
├── logs/                  Logger setup
├── ml/                    Model training, prediction, and Joblib artifacts
├── processing/            Empty package placeholder
├── scheduler/              Standalone periodic weather collector
├── scripts/               Historical import and stored-row enrichment
├── tests/                 Unit tests for four analytics engines
├── visualizations/        Plotly charts backed by SQLite queries
├── README.md              Primary project documentation
└── requirements*.txt      Runtime and test dependencies
```

## Entry points

| Command | Purpose |
| --- | --- |
| `streamlit run app/dashboard.py` | Start the dashboard and initialize its SQLite schema. |
| `python -m database.schema` | Create the SQLite schema for standalone workflows. |
| `python -m scripts.import_historical_data` | Import the hard-coded archive date range for six cities. |
| `python -m scripts.populate_training_data` | Enrich stored observations missing a comfort score. |
| `python -m ml.train_model` | Train and save the comfort classifier from labeled SQLite rows. |
| `python -m scheduler.weather_scheduler` | Start an immediate collection followed by periodic collection. |
| `pytest` | Run the analytics unit tests. |

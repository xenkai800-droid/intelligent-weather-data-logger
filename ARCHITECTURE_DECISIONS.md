# Architecture Notes

This document records the architecture present in the repository. The README is the primary setup and user-facing technical guide.

## Current structure

- `api/` contains separate Open-Meteo clients for current and daily archive data.
- `app/dashboard.py` is a single Streamlit entry point. It coordinates current retrieval, the rule engines, model inference, SQLite-backed charts, and summary queries.
- `analytics/` contains deterministic comfort, anomaly, risk, and recommendation logic.
- `database/` creates and accesses a local SQLite database.
- `scripts/` provides historical import and enrichment command-line workflows.
- `scheduler/` provides a separate foreground process for periodic collection.
- `ml/` trains and loads a Random Forest classifier and checked-in Joblib artifacts.

## Data paths

The dashboard's button fetches current weather and presents rule-based analysis and an ML prediction in that Streamlit run. It does not insert this result into SQLite. Historical imports and the scheduler write weather rows to SQLite. Enrichment fills analytical columns for stored observations. Charts query the local database.

The dashboard creates the database schema at startup. Standalone scripts that access the schema require it to have been initialized first, for example with `python -m database.schema`.

## Implementation constraints

- SQLite keeps setup local and simple; the app has no remote database layer.
- Analytical risk, comfort, anomaly, and recommendation outputs use explicit rules.
- The classifier is separate from those rules, but training targets are generated from the comfort rules.
- Current and historical API clients define their own timeouts. The YAML timeout setting is not wired into them.
- Scheduling runs only when `python -m scheduler.weather_scheduler` is started; it is not launched by Streamlit.

## Known gaps

`ml_predictions` exists in the schema but the application does not write predictions to it. The dashboard's live request does not run anomaly detection. Stored temperature anomalies use a fixed 28°C baseline in the enrichment pipeline.

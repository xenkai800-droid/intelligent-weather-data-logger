# Requirements and Current Coverage

This project is a local Python/Streamlit application. Install runtime dependencies with `python -m pip install -r requirements.txt`; install test tooling with `python -m pip install -r requirements-dev.txt`.

## Runtime requirements

- Python 3.11 or newer, with dependencies pinned in `requirements.txt`.
- Network access for requests to Open-Meteo.
- A local filesystem for SQLite, logs, and model artifacts.
- The checked-in Joblib model and encoder files for dashboard predictions.

## Implemented behavior

| Capability | Current implementation |
| --- | --- |
| Current weather | On-demand dashboard request for six predefined cities. |
| Historical weather | Separate daily archive importer; 2024-01-01 to 2025-12-31 constants. |
| Persistence | SQLite location and weather-observation inserts; dashboard initializes schema. |
| Preprocessing | API field validation and conversion; archive humidity and pressure use fixed defaults. No general cleaning module is implemented. |
| Comfort and risk | Deterministic rule-based engines. |
| Anomaly | Absolute difference from the pipeline's fixed 28°C baseline; flag threshold >10°C. |
| Recommendations | Deterministic text selected by risk label and temperature. |
| ML | Random Forest classification trained from comfort-rule labels; dashboard inference from saved artifacts. |
| Scheduling | Separate foreground process; immediate first collection, then configured interval. |
| Visualization | Streamlit metrics and Plotly historical charts sourced from SQLite. |

## Test coverage

The test suite covers the four analytics engines: comfort, anomaly, risk, and recommendation behavior including input validation. It does not currently cover integration or UI behavior. See [README.md](README.md) for commands and known limitations.

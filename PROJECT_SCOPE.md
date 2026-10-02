# Project Scope

This file describes implemented scope. The setup and usage guide is in [README.md](README.md).

## Implemented

- Current weather retrieval from Open-Meteo for six fixed Indian city coordinates in the dashboard.
- Daily archive retrieval for those cities through a separate importer with a fixed date range.
- Local SQLite storage for locations, observations, derived analytics, and a prediction table schema.
- Deterministic comfort scoring, temperature deviation checks, environmental risk rules, and recommendation text.
- A Random Forest comfort-category model with checked-in model and label-encoder artifacts.
- A Streamlit dashboard with current weather, on-demand analysis and inference, historical charts, and database summary.
- A separate periodic collector that can run continuously when launched manually.

## Boundaries and gaps

- The dashboard does not persist its on-demand current-weather response or model prediction.
- Historical API import, enrichment, training, and periodic collection are separate commands; they are not triggered by the dashboard.
- The historical archive workflow substitutes fixed humidity and pressure values.
- The anomaly enrichment comparison is a constant 28°C, not a dynamic historical baseline.
- Analytics tests do not cover API, database, model, scheduler, or dashboard integration.

## Not part of the current implementation

There is no web service/API exposed by this project, no arbitrary-location input, no automatic scheduler launch from Streamlit, no cloud database, no streaming infrastructure, and no deep-learning component. Ideas such as these should be treated as future work, not existing features.

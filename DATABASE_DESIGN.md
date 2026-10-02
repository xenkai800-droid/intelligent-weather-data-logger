# Database Design

The application uses a local SQLite file at `data/weather.db` by default. `database/schema.py` creates the schema with `CREATE TABLE IF NOT EXISTS`; the dashboard invokes it at startup. The schema can also be created with `python -m database.schema` before running standalone import or scheduler commands.

## Tables

### `locations`

| Column | Type | Constraints / purpose |
| --- | --- | --- |
| `location_id` | INTEGER | Primary key, autoincrement. |
| `city_name` | TEXT | Required display name. |
| `latitude` | REAL | Required coordinate; unique with longitude. |
| `longitude` | REAL | Required coordinate; unique with latitude. |

### `weather_observations`

| Column group | Columns |
| --- | --- |
| Identity and source | `observation_id` primary key, `location_id` foreign key, `timestamp`, `data_source` |
| Measurements | `temperature`, `humidity`, `pressure`, `wind_speed`, `precipitation` |
| Comfort and anomaly | `comfort_score`, `comfort_category`, `anomaly_score`, `anomaly_flag` |
| Risk labels | `heat_stress_risk`, `dehydration_risk`, `outdoor_activity_risk` |
| Recommendations | `hydration_recommendation`, `clothing_recommendation`, `activity_recommendation` |

All columns other than the primary key are nullable in the DDL. The location foreign key uses `ON UPDATE CASCADE` and `ON DELETE SET NULL`.

### `ml_predictions`

`prediction_id` is an autoincrement primary key. `observation_id` references `weather_observations` with `ON DELETE CASCADE`; `prediction_timestamp`, `predicted_comfort_category`, and `prediction_confidence` hold prediction details. The current dashboard does not insert records into this table.

## Persistence behavior

`DatabaseManager` inserts locations and raw observations and reads recent or all observations. It identifies existing locations by name and coordinates or by coordinates alone. Historical import and scheduled collection check for an existing location/timestamp before inserting. The on-demand dashboard fetch only displays its response; it is not persisted.

Local database files and SQLite journal files are excluded from version control.

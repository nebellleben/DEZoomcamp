# Master File

For Data Engineering Zoomcamp Homework 1.

Build the database by running docker compose (refer to [`docker-compose.yaml`](docker-compose.yaml)):
```
docker compose up -d
```

Then ingest the data by the data ingestion stript:
```
uv run python ingest_data.py
```

Refer to this markdown for details of the SQL queries applied: [here](queries.md)
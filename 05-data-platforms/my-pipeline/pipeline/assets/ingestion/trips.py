"""@bruin
name: ingestion.trips
type: python
image: python:3.11

materialization:
  type: table
  strategy: append

connection: duckdb-default

columns:
  - name: pickup_datetime
    type: timestamp
    description: "When the meter was engaged"
  - name: dropoff_datetime
    type: timestamp
    description: "When the meter was disengaged"
@bruin"""

import os
import json
import pandas as pd


def materialize():
    start_date = os.environ["BRUIN_START_DATE"]
    end_date = os.environ["BRUIN_END_DATE"]
    taxi_types = json.loads(os.environ["BRUIN_VARS"]).get("taxi_types", ["yellow"])

    from datetime import datetime
    from dateutil.relativedelta import relativedelta

    start = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
    end = datetime.fromisoformat(end_date.replace("Z", "+00:00"))

    months = []
    current = start.replace(day=1)
    while current <= end:
        months.append((current.year, current.month))
        current += relativedelta(months=1)

    dfs = []
    for taxi_type in taxi_types:
        for year, month in months:
            url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            df = pd.read_parquet(url)
            df["taxi_type"] = taxi_type

            column_mapping = {
                "tpep_pickup_datetime": "pickup_datetime",
                "tpep_dropoff_datetime": "dropoff_datetime",
                "lpep_pickup_datetime": "pickup_datetime",
                "lpep_dropoff_datetime": "dropoff_datetime",
            }
            df = df.rename(columns=column_mapping)
            dfs.append(df)

    final_dataframe = pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

    return final_dataframe

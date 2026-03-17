import dataclasses
import json
from datetime import datetime

import pandas as pd


def ride_deserializer(message):
    return json.loads(message.decode("utf-8"))


@dataclasses.dataclass
class Ride:
    lpep_pickup_datetime: datetime
    lpep_dropoff_datetime: datetime
    PULocationID: int
    DOLocationID: int
    passenger_count: int
    trip_distance: float
    tip_amount: float
    total_amount: float


def ride_from_row(row):
    passenger_count = row["passenger_count"]
    if pd.isna(passenger_count):
        passenger_count = 0
    return Ride(
        lpep_pickup_datetime=row["lpep_pickup_datetime"],
        lpep_dropoff_datetime=row["lpep_dropoff_datetime"],
        PULocationID=row["PULocationID"],
        DOLocationID=row["DOLocationID"],
        passenger_count=passenger_count,
        trip_distance=row["trip_distance"],
        tip_amount=row["tip_amount"],
        total_amount=row["total_amount"],
    )

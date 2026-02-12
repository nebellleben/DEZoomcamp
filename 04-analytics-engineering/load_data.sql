-- Create dataset for NYC taxi rides
CREATE SCHEMA IF NOT EXISTS `de-zoomcamp-485516.taxi_rides_ny`
OPTIONS(
  location = "US"
);

-- Yellow taxi trips table
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-485516.taxi_rides_ny.yellow_external`
OPTIONS (
  format = 'CSV',
  uris = ['gs://de-zoomcamp-485516/taxi_rides_ny/yellow_tripdata_*.csv'],
  skip_leading_rows = 1,
  field_delimiter = ',',
  quote = '"',
  null_marker = ''
);

-- Green taxi trips table
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-485516.taxi_rides_ny.green_external`
OPTIONS (
  format = 'CSV',
  uris = ['gs://de-zoomcamp-485516/taxi_rides_ny/green_tripdata_*.csv'],
  skip_leading_rows = 1,
  field_delimiter = ',',
  quote = '"',
  null_marker = ''
);

-- Native table for Yellow taxi trips (partitioned by pickup date)
CREATE OR REPLACE TABLE `de-zoomcamp-485516.taxi_rides_ny.yellow_trips`
PARTITION BY pickup_date
OPTIONS(
  partition_expiration_days = 3650,
  description = "NYC Yellow Taxi Trip Records"
)
AS
SELECT
  VendorID,
  tpep_pickup_datetime,
  tpep_dropoff_datetime,
  passenger_count,
  trip_distance,
  RatecodeID,
  store_and_fwd_flag,
  PULocationID,
  DOLocationID,
  payment_type,
  fare_amount,
  extra,
  mta_tax,
  tip_amount,
  tolls_amount,
  improvement_surcharge,
  total_amount,
  congestion_surcharge,
  CAST(tpep_pickup_datetime AS DATE) AS pickup_date
FROM
  `de-zoomcamp-485516.taxi_rides_ny.yellow_external`;

-- Native table for Green taxi trips (partitioned by pickup date)
CREATE OR REPLACE TABLE `de-zoomcamp-485516.taxi_rides_ny.green_trips`
PARTITION BY pickup_date
OPTIONS(
  partition_expiration_days = 3650,
  description = "NYC Green Taxi Trip Records"
)
AS
SELECT
  VendorID,
  lpep_pickup_datetime,
  lpep_dropoff_datetime,
  store_and_fwd_flag,
  RatecodeID,
  PULocationID,
  DOLocationID,
  passenger_count,
  trip_distance,
  fare_amount,
  extra,
  mta_tax,
  tip_amount,
  tolls_amount,
  ehail_fee,
  improvement_surcharge,
  total_amount,
  payment_type,
  trip_type,
  congestion_surcharge,
  CAST(lpep_pickup_datetime AS DATE) AS pickup_date
FROM
  `de-zoomcamp-485516.taxi_rides_ny.green_external`;

-- View sample data from yellow trips
SELECT
  COUNT(*) as total_records,
  MIN(pickup_date) as earliest_trip,
  MAX(pickup_date) as latest_trip
FROM
  `de-zoomcamp-485516.taxi_rides_ny.yellow_trips`;

-- View sample data from green trips
SELECT
  COUNT(*) as total_records,
  MIN(pickup_date) as earliest_trip,
  MAX(pickup_date) as latest_trip
FROM
  `de-zoomcamp-485516.taxi_rides_ny.green_trips`;

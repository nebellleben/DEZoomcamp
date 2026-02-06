-- Answer 1

CREATE SCHEMA `de-zoomcamp-485516.yellow_taxi`
  OPTIONS(
    location = "US"
  );

CREATE EXTERNAL TABLE `de-zoomcamp-485516.yellow_taxi.external_yellow_tripdata_2024`
  OPTIONS (
    format = 'PARQUET',
    uris = ['gs://de-zoomcamp-485516/yellow_tripdata_2024-*.parquet']
  );

LOAD DATA INTO `de-zoomcamp-485516.yellow_taxi.yellow_tripdata_2024`
  FROM FILES (
    format = 'PARQUET',
    uris = ['gs://de-zoomcamp-485516/yellow_tripdata_2024-*.parquet']
  );

-- Answer 2

SELECT COUNT(DISTINCT PULocationID) AS distinct_pulocations
FROM de-zoomcamp-485516.yellow_taxi.external_yellow_tripdata_2024;

SELECT COUNT(DISTINCT PULocationID) AS distinct_pulocations
FROM de-zoomcamp-485516.yellow_taxi.yellow_tripdata_2024;

-- Answer 3

SELECT PULocationID
FROM de-zoomcamp-485516.yellow_taxi.yellow_tripdata_2024
LIMIT 1000; --155.12MB

SELECT PULocationID, DOLocationID
FROM de-zoomcamp-485516.yellow_taxi.yellow_tripdata_2024
LIMIT 1000; --310.24MB

-- Answer 4

SELECT COUNT(*) 
FROM de-zoomcamp-485516.yellow_taxi.yellow_tripdata_2024 
WHERE fare_amount = 0;


-- Answer 6

CREATE OR REPLACE TABLE `de-zoomcamp-485516.yellow_taxi.yellow_tripdata_2024_partitioned`
  PARTITION BY DATE(tpep_dropoff_datetime)  -- Filter column
  CLUSTER BY VendorID                        -- Order/group column
  AS
  SELECT * FROM `de-zoomcamp-485516.yellow_taxi.yellow_tripdata_2024`;

SELECT COUNT(DISTINCT VendorID)
FROM de-zoomcamp-485516.yellow_taxi.yellow_tripdata_2024
WHERE tpep_dropoff_datetime >= '2024-03-01' AND tpep_dropoff_datetime < '2024-03-16'; --310.24MB;

SELECT COUNT(DISTINCT VendorID)
FROM de-zoomcamp-485516.yellow_taxi.yellow_tripdata_2024_partitioned
WHERE tpep_dropoff_datetime >= '2024-03-01' AND tpep_dropoff_datetime < '2024-03-16'; --26.84MB


-- Answer 9
SELECT COUNT(*)
FROM de-zoomcamp-485516.yellow_taxi.yellow_tripdata_2024;

-- 0MB
-- BigQuery maintains table metadata, so it doesn't scan the actual data — it just reads the stored row count from metadata.

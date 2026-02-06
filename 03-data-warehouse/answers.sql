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

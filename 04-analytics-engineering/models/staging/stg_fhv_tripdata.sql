-- Question 6: Staging Model for FHV Data
-- This is a staging model for For-Hire Vehicle (FHV) trip data for 2019
-- It filters out records with NULL dispatching_base_num and renames fields to match project conventions

{{
    config(
        materialized='table'
    )
}}

-- Filter out records where dispatching_base_num IS NULL or empty
-- Rename fields to match project naming conventions
-- Convert string timestamps to TIMESTAMP type
SELECT 
    dispatching_base_num,
    CAST(PUlocationID AS INT64) AS pickup_location_id,
    CAST(DOlocationID AS INT64) AS dropoff_location_id,
    Affiliated_base_number,
    CAST(NULL AS TIMESTAMP) AS request_datetime,
    CAST(NULL AS TIMESTAMP) AS on_scene_datetime,
    CAST(pickup_datetime AS TIMESTAMP) AS pickup_datetime,
    CAST(dropOff_datetime AS TIMESTAMP) AS dropoff_datetime,
    SR_Flag
FROM {{ source('raw', 'fhv_tripdata_2019') }}
WHERE dispatching_base_num IS NOT NULL 
  AND dispatching_base_num != ''
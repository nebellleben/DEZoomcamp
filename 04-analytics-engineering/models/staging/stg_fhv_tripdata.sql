-- Question 6: Staging Model for FHV Data
-- This is a staging model for For-Hire Vehicle (FHV) trip data for 2019
-- It filters out records with NULL dispatching_base_num and renames fields to match project conventions

{{
    config(
        materialized='table'
    )
}}

-- Filter out records where dispatching_base_num IS NULL
-- Rename fields to match project naming conventions
SELECT 
    dispatching_base_num,
    PUlocationID AS pickup_location_id,
    DOlocationID AS dropoff_location_id,
    Affiliated_base_number,
    request_datetime,
    on_scene_datetime,
    pickup_datetime,
    dropoff_datetime,
    SR_Flag
FROM {{ ref('fhv_trips_2019') }}
WHERE dispatching_base_num IS NOT NULL
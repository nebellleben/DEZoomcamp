-- Question 6: Count of Records in stg_fhv_tripdata
-- This query counts the total number of records in the stg_fhv_tripdata model after filtering

SELECT 
    COUNT(*) as total_records
FROM {{ ref('stg_fhv_tripdata') }};
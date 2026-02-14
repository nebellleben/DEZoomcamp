-- Question 5: Green Taxi Trip Counts (October 2019)
-- This query calculates the total number of trips for Green taxis in October 2019

SELECT 
    SUM(total_monthly_trips) as total_green_trips_october_2019
FROM {{ ref('fct_monthly_zone_revenue') }}
WHERE 
    service_type = 'Green'  -- Filter for Green taxi trips only
    AND month_id = '2019-10-01'  -- Filter for October 2019 (assuming month_id is the first day of each month);
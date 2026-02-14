-- Question 3: Counting Records in fct_monthly_zone_revenue
-- This query counts the total number of records in the fct_monthly_zone_revenue model

SELECT 
    COUNT(*) as total_records
FROM {{ ref('fct_monthly_zone_revenue') }};
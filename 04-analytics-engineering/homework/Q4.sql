-- Question 4: Best Performing Zone for Green Taxis (2020)
-- This query finds the pickup zone with the highest total revenue for Green taxi trips in 2020

SELECT 
    pickup_zone,
    revenue_monthly_total_amount
FROM {{ ref('fct_monthly_zone_revenue') }}
WHERE 
    service_type = 'Green'  -- Filter for Green taxi trips only
    AND YEAR(month_id) = 2020  -- Filter for 2020 data
ORDER BY 
    revenue_monthly_total_amount DESC  -- Order by highest revenue first
LIMIT 1;  -- Get only the top performing zone
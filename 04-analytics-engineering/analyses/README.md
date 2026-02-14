# Data Engineering Zoomcamp - Homework 4 Solutions (Q3-Q6)

This directory contains SQL queries for questions 3-6 from the Analytics Engineering with dbt homework.

## Files Overview

### Q3.sql
**Question**: Counting Records in `fct_monthly_zone_revenue`
- Uses `{{ ref('fct_monthly_zone_revenue') }}` to reference the dbt model
- Simple COUNT(*) to get total records

### Q4.sql
**Question**: Best Performing Zone for Green Taxis (2020)
- Filters for service_type = 'Green' and year 2020
- Orders by revenue_monthly_total_amount DESC
- Uses LIMIT 1 to get the top performing zone

### Q5.sql
**Question**: Green Taxi Trip Counts (October 2019)
- Filters for Green taxis and October 2019 (month_id = '2019-10-01')
- Sums total_monthly_trips across all zones
- Assumes month_id format is YYYY-MM-01 (first day of month)

### stg_fhv_tripdata.sql
**Question 6 Part 1**: Staging model for FHV data
- Filters out records where dispatching_base_num IS NULL
- Renames fields using snake_case convention:
  - PUlocationID → pickup_location_id
  - DOlocationID → dropoff_location_id
- References source data using {{ source() }}

### Q6.sql
**Question 6 Part 2**: Count records in staging model
- References the stg_fhv_tripdata model created above
- Counts records after filtering

## dbt References Used

- `{{ ref('model_name') }}` - References other dbt models
- `{{ source('source_name', 'table_name') }}` - References raw source data
- No hardcoded schema or table names as per requirements

## Notes

- All queries include comments explaining the purpose and logic
- Assumes standard dbt project structure with proper sources.yml configuration
- Q6 assumes FHV data has been loaded and properly configured in sources.yml
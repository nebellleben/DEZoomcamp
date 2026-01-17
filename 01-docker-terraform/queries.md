## Copies all queries used in Q3-6 here:

### Q3
- I first inspected all dates to confirm the range of dates
`SELECT DISTINCT CAST (lpep_pickup_datetime AS DATE) AS dates FROM public.green_taxi_trips ORDER BY dates

- Then the following queried performed to get answers for "For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?"
```
SELECT COUNT(*)
FROM public.green_taxi_trip
WHERE lpep_pickup_datetime >= '2025-11-01' AND lpep_pickup_datetime < '2025-12-01' AND trip_distance <= 1;
```
- Answer: 8007

### Q4
- "Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles."
```
SELECT CAST (lpep_pickup_datetime AS DATE)
FROM green_taxi_trips
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;
```
- Answer: 2025-11-14

### Q5

- "Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?"
```
```

### Q6

- "For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?"
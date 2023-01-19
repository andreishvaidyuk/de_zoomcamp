Question 1:
```text
--iidfile string
```
Question 2:
```text
3 packages:
Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4 
```
Question 3:
```text
select 
	count (1) as count
from green_taxi_data
where
	CAST (lpep_pickup_datetime as DATE) = '2019-01-15' AND
	CAST (lpep_dropoff_datetime as DATE) = '2019-01-15'
```
Question 4:
```text
Select
 	CAST (lpep_pickup_datetime as DATE),
 	trip_distance
from green_taxi_data
order by trip_distance desc
```
Question 5:
```text
select 
    count (1) as count
from green_taxi_data
where
 	CAST (lpep_pickup_datetime as DATE) = '2019-01-01' AND
 	passenger_count = 2
```
Question 6:
```text
select 
	tip_amount,
	zpu."Zone" as pickup_loc,
	zdo."Zone" as dropoff_loc 
from 
	green_taxi_data as d,
	zones as zpu,
	zones as zdo
where 
	d."PULocationID" = zpu."LocationID" and
	d."DOLocationID" = zdo."LocationID" and
	zpu."Zone" = 'Astoria'
order by
	tip_amount desc
limit 10
```
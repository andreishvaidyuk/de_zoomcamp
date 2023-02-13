# additional queries
# view table data
SELECT * FROM `spheric-crow-375309.dezoomcamp_europe.external_yellow_tripdata` LIMIT 10;


# create partitioned table on field "dispatching_base_num"
CREATE OR REPLACE TABLE `spheric-crow-375309.dezoomcamp_europe.fhv_partitioned_tripdata`
PARTITION BY DATE(pickup_datetime)
AS (SELECT * FROM `spheric-crow-375309.dezoomcamp_europe.external_fhv_tripdata`);


# IMPACT of partitioning
SELECT count(affiliated_base_number) FROM  `spheric-crow-375309.dezoomcamp_europe.fhv_nonpartitioned_tripdata`
WHERE pickup_datetime BETWEEN '2019-03-01' AND '2019-03-31'
  AND dispatching_base_num IN ('B00987', 'B02279', 'B02060');

SELECT count(affiliated_base_number) FROM `spheric-crow-375309.dezoomcamp_europe.fhv_partitioned_tripdata`
WHERE dropoff_datetime BETWEEN '2019-03-01' AND '2019-03-31'
  AND dispatching_base_num IN ('B00987', 'B02279', 'B02060');


# look into partiotions
SELECT table_name, partition_id, total_rows
FROM  `spheric-crow-375309.dezoomcamp_europe.INFORMATION_SCHEMA.PARTITIONS`
Where table_name = 'fhv_partitioned_tripdata'
order by total_rows desc;




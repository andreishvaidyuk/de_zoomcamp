Prepare tables
```text
# create external table
CREATE OR REPLACE EXTERNAL TABLE `spheric-crow-375309.dezoomcamp_europe.external_fhv_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dtc_data_lake_spheric-crow-375309/data\\yellow\\fhv_tripdata_2019-*.csv.gz']
);

# create BQ table (not partition or cluster)
CREATE OR REPLACE TABLE `spheric-crow-375309.dezoomcamp_europe.fhv_nonpartitioned_tripdata`
AS SELECT * FROM `spheric-crow-375309.dezoomcamp_europe.external_fhv_tripdata`;
```

Question 1:
```text
# count number of rows
SELECT count(affiliated_base_number) FROM `spheric-crow-375309.dezoomcamp_europe.external_fhv_tripdata`;
```

Question 2:
```text
# external table
SELECT count(distinct(affiliated_base_number)) FROM `spheric-crow-375309.dezoomcamp_europe.external_fhv_tripdata`;
# BQ table
SELECT count(distinct(affiliated_base_number)) FROM `spheric-crow-375309.dezoomcamp_europe.fhv_nonpartitioned_tripdata`;
```
Question 3:
```text
# count number of rows
SELECT count(*) FROM `spheric-crow-375309.dezoomcamp_europe.external_fhv_tripdata`
where PUlocationID is NULL and DOlocationID is Null;
```
Question 4:
```text
Partition by pickup_datetime Cluster on affiliated_base_number
```
Question 5:
```text
# create partitioned  on field "pickup_datetime" and clustere on field "dispatching_base_num" table to check performance
CREATE OR REPLACE TABLE `spheric-crow-375309.dezoomcamp_europe.fhv_partitioned_clustered_tripdata`
PARTITION BY DATE(pickup_datetime)
CLUSTER BY dispatching_base_num AS (
  SELECT * FROM `spheric-crow-375309.dezoomcamp_europe.external_fhv_tripdata`
);

# non-partitioned table
SELECT count(distinct(affiliated_base_number)) FROM `spheric-crow-375309.dezoomcamp_europe.fhv_nonpartitioned_tripdata`
WHERE pickup_datetime BETWEEN '2019-03-01' AND '2019-03-31';

# partitioned table
SELECT count(distinct(affiliated_base_number)) FROM `spheric-crow-375309.dezoomcamp_europe.fhv_partitioned_clustered_tripdata`
WHERE pickup_datetime BETWEEN '2019-03-01' AND '2019-03-31';
```
Question 6:
```text
GCP Bucket
```
Question 7:
```text
False
```
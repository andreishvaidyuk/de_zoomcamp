Question 1:
```text
# create external table
CREATE OR REPLACE EXTERNAL TABLE `spheric-crow-375309.dezoomcamp_europe.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://dtc_data_lake_spheric-crow-375309/data\\yellow\\fhv_tripdata_2019-*.csv.gz']
);

# count nomber of rows
SELECT count(affiliated_base_number) FROM `spheric-crow-375309.dezoomcamp_europe.external_yellow_tripdata`;
```
Question 2:
```text
SELECT count(distinct(affiliated_base_number)) FROM `spheric-crow-375309.dezoomcamp_europe.external_yellow_tripdata`
```
Question 3:
```text
# count number of rows
SELECT count(*) FROM `spheric-crow-375309.dezoomcamp_europe.external_yellow_tripdata`
where PUlocationID is NULL and DOlocationID is Null;
```
Question 4:
```text
Partition by pickup_datetime Cluster on affiliated_base_number
```
Question 5:
```text
SELECT count(distinct(affiliated_base_number)) FROM `spheric-crow-375309.dezoomcamp_europe.external_yellow_tripdata`
WHERE pickup_datetime BETWEEN '2019-03-01' AND '2019-03-31';

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
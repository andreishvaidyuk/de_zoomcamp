## Docker and SQL

Notes I used for preparing the videos: [link](https://docs.google.com/document/d/e/2PACX-1vRJUuGfzgIdbkalPgg2nQ884CnZkCg314T_OBq-_hfcowPxNIA0-z5OtMTDzuzute9VBHMjNYZFTCc1/pub)


## Commands 

All the commands from the video

Downloading the data

```bash
wget https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv
```

### Running Postgres with Docker

#### Windows

Running postgres on windows (note the full path)

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v c:/Users/ashva/git/de_zoomcamp/week_1/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5431:5432 \
  postgres:13
```

If you have the following error:

```
docker: Error response from daemon: invalid mode: \Program Files\Git\var\lib\postgresql\data.
See 'docker run --help'.
```

Change the mouning path. Replace it with the following:

```
-v //c/Users/...:/var/lib/postgresql/data
```

If you see that `ny_taxi_postgres_data` is empty after running
the container, try these:

* Deleting the folder and running Docker again (Docker will re-create the folder)
* Give "Full Control" to the folder I am using as local/source mounting directory and adding it to the sharing group "Everyone" (right click on folder> Properties> Sharing> Advanced Settings)
* Verify the docker-daemon C drive sharing is activated (with Linux mounting system, so I need to use -v //c/Users/...:/var/lib/postgresql/data to access my drive and properly mount it on the container)


### CLI for Postgres

Installing pgcli

```bash
pip install pgcli
```

If you have problems installing pgcli with the command above, try this:

```bash
conda install -c conda-forge pgcli
pip install -U mycli
```

Using pgcli to connect to postgres

```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

If you have a problem 
```
connection to server at "localhost" (::1), port 5432 failed: FATAL:  password authentication
failed for user "root" .
```

change the port on the host to 5431

Dataset:

* https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page
* https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

Upload process described in file `upload-data.ipynb`.


Running pgAdmin

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```
After that we need to go to `localhost:8080`, enter email and password. Now we need to create a new server. 
But server will not created because Postgres and PgAdmin are now in different containers.

### Running Postgres and pgAdmin together

Create a network to be able to connect Postgres and PgAdmin (they are now in different containers).

```bash
docker network create pg-network
```

Run Postgres (change the path)

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v //c/Users/ashva/git/de_zoomcamp/week_1/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5431:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```

Run pgAdmin

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

Now it works fine.

### Data ingestion

Running locally

Firstly prepare script `ingest_data.py`

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-01.csv.gz"

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_data \
  --url=${URL}
```

Build the image

```bash
docker build -t taxi_ingest:v001 .
```

Run the script with Docker
We need to change "host" from "local" to "pg-database".

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-01.csv.gz"

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_data \
    --url=${URL}
```

Ingest data with zones.
```bash
docker build -t zones_ingest:v001 .

URL="https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv"

docker run -it \
  --network=pg-network \
  zones_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=zones \
    --url=${URL}
```

After that data will available through PgAdmin.

### Docker-Compose 

Prepare `docker-compose.yaml` file with all configuration in one file.

Run it:

```bash
docker-compose up
```

Run in detached mode:

```bash
docker-compose up -d
```

Shutting it down:

```bash
docker-compose down
```

Note: to make pgAdmin configuration persistent, mount a volume to the `/var/lib/pgadmin` folder:

```yaml
services:
  pgadmin:
    image: dpage/pgadmin4
    volumes:
      - ./data_pgadmin:/var/lib/pgadmin
    ...
```


### SQL 

Some queries:
```text
select *
From yellow_taxi_data
LIMIT 100
```

Select from 2 tables
```text
select 
	* 
from 
	yellow_taxi_data as d,
	zones as zpu,
	zones as zdo
where 
	d."PULocationID" = zpu."LocationID" and
	d."DOLocationID" = zdo."LocationID"
limit 100
```

```text
select 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	concat(zpu."Borough", '/', zpu."Zone") as pickup_loc,
	concat(zdo."Borough", '/', zdo."Zone") as dropoff_loc 
from 
	yellow_taxi_data as d,
	zones as zpu,
	zones as zdo
where 
	d."PULocationID" = zpu."LocationID" and
	d."DOLocationID" = zdo."LocationID"
limit 100
```
Same result with JOIN statement
```text
select 
	tpep_pickup_datetime,
	tpep_dropoff_datetime,
	total_amount,
	concat(zpu."Borough", '/', zpu."Zone") as pickup_loc,
	concat(zdo."Borough", '/', zdo."Zone") as dropoff_loc 
from 
	yellow_taxi_data as d 
		join zones as zpu
			on d."PULocationID" = zpu."LocationID"
		join zones as zdo
			on d."DOLocationID" = zdo."LocationID"
limit 100
```

GROUP BY and ORDER BY statements
```text
select 
	CAST (tpep_dropoff_datetime as DATE) as day,
	total_amount,
	count(1) as count
	max(total_amount),
	max(passenger_count)
from
	yellow_taxi_data as d 
GROUP BY 
	CAST (tpep_dropoff_datetime as DATE)
ORDER BY
	"count" DESC
```
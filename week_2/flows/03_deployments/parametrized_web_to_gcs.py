from pathlib import Path
import pandas as pd
from time import time
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from prefect.tasks import task_input_hash
from datetime import timedelta


@task(retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def fetch(dataset_url: str) -> pd.DataFrame:
    """Read taxi data from web into pandas dataFrame"""

    # df = pd.read_csv(dataset_url)
    # return df

    df_iter = pd.read_csv(dataset_url, iterator=True, chunksize=100000)  # compression='gzip',
    df_all = next(df_iter)

    try:
        df_all.tpep_pickup_datetime = pd.to_datetime(df_all.tpep_pickup_datetime)
        df_all.tpep_dropoff_datetime = pd.to_datetime(df_all.tpep_dropoff_datetime)
    except:
        pass
    # for Green Taxi
    try:
        df_all.lpep_pickup_datetime = pd.to_datetime(df_all.lpep_pickup_datetime)
        df_all.lpep_dropoff_datetime = pd.to_datetime(df_all.lpep_dropoff_datetime)
    except:
        pass

    while True:
        try:
            t_start = time()
            df = next(df_iter)

            # for Yellow Taxi
            try:
                df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
                df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            except:
                pass
            # for Green Taxi
            try:
                df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
                df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
            except:
                pass

            df_all = pd.concat([df_all, df])
            # df.to_sql(name=table_name, con=engine, if_exists='append')
            t_end = time()

            print('inserted another chunk ..., took %.3f second' % (t_end - t_start))

        except StopIteration:
            print("Finished ingesting data into the postgres database")
            break

    return df_all


@task(log_prints=True)
def clean(df: pd.DataFrame, color: str) -> pd.DataFrame:
    """Fix dtype issues"""

    # for Yellow Taxi
    if color == "yellow":
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    else:
        df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
        df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)

    print(df.head(2))
    print(f"columns: {df.dtypes}")
    print(f"rows: {len(df)}")
    return df


@task()
def write_local(df: pd.DataFrame, color: str, dataset_file: str) -> Path:
    """Write DataFrame ouy locally as parquet file"""
    path = Path(f"data/{color}/{dataset_file}.parquet")
    df.to_parquet(path, compression="gzip")
    return path


@task()
def write_gcs(path: Path) -> None:
    """Upload file into GCS"""
    gcs_block = GcsBucket.load("zoom-gcs")      # name of GCS Bucket
    gcs_block.upload_from_path(from_path=f"{path}", to_path=path)
    return


@flow()
def etl_web_to_gcs(year: int, month: int, color: str) -> None:
    """The main ETL function"""
    dataset_file = f"{color}_tripdata_{year}-{month:02}"
    dataset_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{color}/{dataset_file}.csv.gz"

    df = fetch(dataset_url)
    df_clean = clean(df, color)
    path = write_local(df_clean, color, dataset_file)
    write_gcs(path)


@flow()
def etl_parent_flow(months: list[int] = [2, 3], year: int = 2019, color: str = "yellow"):
    for month in months:
        etl_web_to_gcs(year, month, color)


if __name__ == '__main__':
    color = "green"
    months = [4]
    year = 2019
    etl_parent_flow(months, year, color)

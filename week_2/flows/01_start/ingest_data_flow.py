#!/usr/bin/env python
# coding: utf-8

import os
import argparse

from time import time
from datetime import timedelta
import pandas as pd
from sqlalchemy import create_engine
from prefect import flow, task
from prefect.tasks import task_input_hash
from prefect_sqlalchemy import SqlAlchemyConnector


@task(log_prints=True, retries=3, cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
def extract_data(url):
    # the backup files are gzipped, and it's important to keep the correct extension
    # for pandas to be able to open the file
    if url.endswith('.csv.gz'):
        csv_name = 'green_tripdata_2020-01.csv.gz'
    else:
        csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")
    df_iter = pd.read_csv(csv_name,  iterator=True, chunksize=100000)  #compression='gzip',
    df = next(df_iter)
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    # while True:
    #     try:
    #         t_start = time()
    #         df = next(df_iter)
    #         df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    #         df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    #         df.to_sql(name=table_name, con=engine, if_exists='append')
    #         t_end = time()
    #
    #         print('inserted another chunk ..., took %.3f second' % (t_end - t_start))
    #
    #     except StopIteration:
    #         print("Finished ingesting data into the postgres database")
    #         break

    return df


@task(log_prints=True)
def transform_data(df):
    print(f"pre: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    df = df[df['passenger_count'] != 0]
    print(f"post: missing passenger count: {df['passenger_count'].isin([0]).sum()}")
    return df


@task(log_prints=True, retries=3)
def load_data(table_name, df):
    # block created in Prefect UI (Orion)
    connection_block = SqlAlchemyConnector.load("postgres-connector")
    with connection_block.get_connection(begin=False) as engine:
        df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
        df.to_sql(name=table_name, con=engine, if_exists='append')


@flow(name="Subflow", log_prints=True)
def log_subflow(table_name:str):
    print(f"Logging Subflow for: {table_name}")


@flow(name="Ingest Data")
def main_flow(table_name):
    user = "postgres"
    password = "admin"
    host = "localhost"
    port = "5432"
    db = "ny_taxi"
    csv_url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green/green_tripdata_2020-01.csv.gz"

    log_subflow(table_name)
    raw_data = extract_data(csv_url)
    data = transform_data(raw_data)
    load_data(table_name, data)


if __name__ == '__main__':
    main_flow("green_taxi_trips")

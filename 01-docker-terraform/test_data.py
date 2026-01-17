#!/usr/bin/env python
# coding: utf-8

# ## Test Injection of Data
# 
# - This note book try to import parquet file into postgreSQL database
# - Remember to implement the click part to take in command line parameters
# - When done it will be converted to script using nbconvert

# In[1]:


import pandas as pd
import click
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import pyarrow.parquet as pq


#pg_user = 'postgres'
#pg_pass = 'postgres'
#pg_host = 'localhost'
#pg_port = '5433'
#pg_db = 'ny_taxi'
#target_table = 'green_taxi_trips'

@click.command()
@click.option('--pg-user', default='postgres', help='PostgreSQL user')
@click.option('--pg-pass', default='postgres', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5433, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
#@click.option('--year', default=2021, type=int, help='Year of the data')
#@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--target-table', default='green_taxi_trips', help='Target table name')
#@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading CSV')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table):
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    first = True
    preview_df = None

    parquet_path = "./green_tripdata_2025-11.parquet"
    parquet_file = pq.ParquetFile(parquet_path)

    for batch in tqdm(parquet_file.iter_batches(batch_size=100000)):
        df_chunk = batch.to_pandas()

        if first:
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace'
            )
            preview_df = df_chunk.head()
            first = False

        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append'
        )

    if preview_df is not None:
        print(preview_df)



if __name__ == '__main__':
    run()


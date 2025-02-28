import argparse
import pandas as pd
from time import time 
import os
import pyarrow.parquet as pq
from sqlalchemy import create_engine
import sys 


def main(params):
    user=params.user
    password=params.password
    host=params.host
    port=params.port
    db=params.db
    table_name=params.table_name
    url=params.url

    file_name=url.rsplit('/',1)[-1].strip()
    print(f'Download file name: {file_name}')
    os.system(f'wget ${url} -O yellow_tripdata_2024-01.parquet')
    #create engine
    engine=create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    if '.csv' in file_name :
        df=pd.read_csv(file_name,nrow=10)
        df_iter=pd.read_csv(file_name, chunksize=100000, iterator=True)
    elif '.parquet' in file_name:
        file=pq.ParquetFile(file_name)
        df=next(file.iter_batches(batch_size=10)).to_pandas()
        df_iter=file.iter_batches(batch_size=100000)
    else: 
        print('Error. Only .csv or .parquet files allowed.')
        sys.exit()
        # Create the table
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    t_start = time()
    count = 0
    
    for batch in df_iter:
        count+=1
        if '.parquet' in file_name:
            batch_df = batch.to_pandas()
        else:
            batch_df = batch
        print(f'inserting batch {count}...')
        b_start = time()
        
        batch_df.to_sql(name=table_name,con=engine, if_exists='append')
    b_end = time()
    print(f'inserted! time taken {b_end-b_start:10.3f} seconds.\n')

# Insert values into the table 
if __name__=='__main__': 
    parser=argparse.ArgumentParser(description='Loading data from .paraquet file link to a Postgres datebase.')
    parser.add_argument('--user', help='Username for Postgres.')
    parser.add_argument('--password', help='Password to the username for Postgres.')
    parser.add_argument('--host', help='Hostname for Postgres.')
    parser.add_argument('--port', help='Port for Postgres connection.')
    parser.add_argument('--db', help='Databse name for Postgres')
    parser.add_argument('--table_name', help='Destination table name for Postgres.')
    parser.add_argument('--url', help='URL for .paraquet file.')
    args = parser.parse_args()
    main(args)
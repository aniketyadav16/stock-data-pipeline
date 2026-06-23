# Y5MTFA3OT2V6F3SD

import pandas as pd
import requests
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
import hashlib
import click
from sqlalchemy import text

@click.command()
@click.option('--alpha', help= 'Alpha_Api')
@click.option('--symbol', default='ibm', help='Stock symbol to fetch data for')
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='pipelino', help='PostgreSQL database name')

def run(alpha, symbol, pg_user, pg_pass, pg_host, pg_port, pg_db):

    symbol = symbol.upper()

    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={alpha}'
    r = requests.get(url)
    data = r.json()['Time Series (Daily)']
    df = pd.DataFrame.from_dict(data, orient='index', dtype = 'float32')

    df.columns = df.columns.str.replace(r'^\d+\.\s*', '', regex=True)
    df['symbol'] = symbol
    df['load_time'] = pd.Timestamp.now()

    df['hash_id'] = (df['symbol'] + df.index.astype(str)).apply(lambda x: hashlib.md5(x.encode()).hexdigest())
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    df.to_sql(name='staging_stock_data', con=engine, if_exists='replace')
    print("-----------------------------------------------------------------------------------------------------------")
    print("-----Data inserted successfully, Another minor proof that Aniket's a Genius (in his own weird life :>)-----")
    print("-----------------------------------------------------------------------------------------------------------")
    print("##################### Now Merging Data into Productionnnn, I'm a robottt #####################")
    print("-----------------------------------------------------------------------------------------------------------")

    upsert_query = """
        INSERT INTO prod_stock_data (symbol, index, open, high, low, close, volume, hash_id, load_time)
        SELECT symbol, index, open, high, low, close, volume, hash_id, load_time
        FROM staging_stock_data
        ON CONFLICT (hash_id) 
        DO UPDATE SET 
            open = EXCLUDED.open,
            high = EXCLUDED.high,
            low = EXCLUDED.low,
            close = EXCLUDED.close,
            volume = EXCLUDED.volume;
    """

    with engine.begin() as connection:
        connection.execute(text(upsert_query))
        
        connection.execute(text("TRUNCATE TABLE staging_stock_data;"))
    print("-----------------------------------------------------------------------------------------------------------")
    print("--------------- Data successfully merged into Production! BoooM! Idempotency you PoS! ---------------------")
    print("-----------------------------------------------------------------------------------------------------------")
    pass    
if __name__ == "__main__":
    run()  
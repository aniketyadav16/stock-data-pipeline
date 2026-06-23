# Y5MTFA3OT2V6F3SD

import pandas as pd
import requests
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
load_dotenv()
import hashlib

API_KEY = os.getenv("ALPHA_API")

symbol=input("Enter the stock symbol: ")
symbol = symbol.upper()
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
r = requests.get(url)
data = r.json()['Time Series (Daily)']
df = pd.DataFrame.from_dict(data, orient='index', dtype = 'float32')

df.columns = df.columns.str.replace(r'^\d+\.\s*', '', regex=True)
df['symbol'] = symbol
df['load_time'] = pd.Timestamp.now()

df['hash_id'] = (df['symbol'] + df.index.astype(str)).apply(lambda x: hashlib.md5(x.encode()).hexdigest())
engine = create_engine('postgresql+psycopg://root:root@localhost:5432/pipelino')

df.to_sql(name='stock_data', con=engine, if_exists='replace')

print("Data inserted successfully, Another minor proof that Aniket's a Genius (in his own ways :> )")
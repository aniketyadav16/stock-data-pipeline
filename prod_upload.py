from sqlalchemy import text
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg://root:root@localhost:5432/pipelino')
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

print("Data successfully merged into Production! BoooM! Idempotency you PoS!")
CREATE TABLE IF NOT EXISTS prod_stock_data (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    index DATE NOT NULL,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    load_time TIMESTAMP,
    hash_id VARCHAR(64) UNIQUE NOT NULL, -- UNIQUE constraint is required for ON CONFLICT
    _updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create the Staging Table
CREATE TABLE IF NOT EXISTS staging_stock_data (
    symbol VARCHAR(10),
    index DATE,
    open NUMERIC,
    high NUMERIC,
    low NUMERIC,
    close NUMERIC,
    volume BIGINT,
    hash_id VARCHAR(64),
    load_time TIMESTAMP,
    _loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create the Stored Procedure (The "In-Postgres" Logic)
-- This bundles the Merge and the Truncate into one secure transaction.
CREATE OR REPLACE PROCEDURE process_staging_data()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Step A: Upsert the data (Idempotent Merge)
    INSERT INTO prod_stock_data (symbol, index, open, high, low, close, volume, hash_id, load_time)
    SELECT symbol, index, open, high, low, close, volume, hash_id, load_time
    FROM staging_stock_data
    ON CONFLICT (hash_id) 
    DO UPDATE SET 
        open = EXCLUDED.open,
        high = EXCLUDED.high,
        low = EXCLUDED.low,
        close = EXCLUDED.close,
        volume = EXCLUDED.volume,
        _updated_at = CURRENT_TIMESTAMP; -- Track when it was updated

    -- Step B: Empty the staging table
    TRUNCATE TABLE staging_stock_data;

    -- Note: If anything fails in Step A, Step B will NOT run. 
    -- Postgres rolls back the whole transaction automatically!
END;
$$;
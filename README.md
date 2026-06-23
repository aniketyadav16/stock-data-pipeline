# Pipelino
### A lame but smort project to prove my skills to the ruthless world of engineers

#### A docker container that lets you collect and store stocks data from alpha vantage api. 

#### inputs: alpha (alpha api)
####       : symbol (stock symbol for the targeted stock)
####       : pg-user (postgres user)  
####       : pg-pass (postgres database password)  
####       : pg-host (postgres database host)  
####       : pg-port (postgres database port)  
####       : pg-db (postgres database name)


#### Data is stored in a postgres database with two tables: staging_stock_data and prod_stock_data. 

#### The data is first inserted into the staging table and then merged into the production table using an upsert operation. 

#### The staging table is truncated after the merge to ensure idempotency. Data is stored in the production table with a hash_id column to ensure uniqueness and prevent duplicates. hash_id is an augmented column made using the md5 hashing algo.

#### The project uses the following libraries: requests, pandas, sqlalchemy, click.

#### For orchestration the project uses kestra.


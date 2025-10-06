from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import pandas as pd
import time
from sqlalchemy import create_engine, text, inspect
import logging

# Create connection to Postgres Database
POSTGRES_CONN = "postgresql+psycopg2://airflow:airflow@postgres:5432/green_drive"

# Load raw vehicle data into Postgres
def bronze_load_vehicles():
    # -- 1. If the table DOES NOT exist (initial run/fresh start), it uses the 
    # manual DROP/PAUSE/CREATE sequence to avoid the PostgreSQL
    # pg_type UniqueViolation error.
    # -- 2. If the table DOES exist (regeneration/warm run), it APPENDS new data.

    engine = create_engine(POSTGRES_CONN)
    table_name = "bronze_vehicles"
    schema_name = "public"
    
    # Reading CSV (Note: DataFrame is created before inspection)
    df = pd.read_csv("/opt/airflow/data/vehicles.csv") 
    
    # Create an Inspector object to introspect the database schema (tables, columns, etc.)
    inspector = inspect(engine)
    
    # Does the table exist?
    if not inspector.has_table(table_name, schema=schema_name):
        # -- 1: INITIAL RUN / TABLE DOES NOT EXIST
        logging.info(f"[{table_name}] Table not found. Executing initial CREATE sequence.")
        
        # 1. Manual Drop (uses engine.begin() to manage the transaction and commit)
        # We drop the table first using a transaction block (engine.begin())
        # to ensure the commit happens immediately, freeing the metadata lock.
        with engine.begin() as connection:
            drop_sql = text(f"DROP TABLE IF EXISTS {schema_name}.{table_name} CASCADE;") 
            connection.execute(drop_sql)
        
        logging.info("DROP completed. Pausing 1 second for internal metadata cleanup.")

        # 2. PAUSE (to prevent UniqueViolation)
        time.sleep(1) 
        
        # 3. CREATE TABLE (since I dropped it, I use if_exists="fail")
        df.to_sql(
            table_name,
            engine,
            if_exists="fail", # Will create the table since it was just dropped
            schema=schema_name,
            index=False)
        logging.info(f"Successfully performed initial creation and load into {table_name}.")

    else:
        # -- 2: TABLE EXISTS
        logging.info(f"[{table_name}] Table found. Checking for new rows to append.")

        # Read existing IDs from bronze
        existing_ids = pd.read_sql(f"SELECT id FROM {table_name}", engine)

        # Keep only new rows
        df_new = df[~df['id'].isin(existing_ids['id'])]
        
        # Append only if there are new rows
        if not df_new.empty:
            df_new.to_sql(
                table_name,
                engine,
                if_exists="append",
                schema=schema_name,
                index=False
            )
            logging.info(f"Appended {len(df_new)} new rows to {table_name}")
        else:
            logging.info(f"No new rows to append to {table_name}")

# Clean and normalize vehicle data
def silver_transform_vehicles():
    engine = create_engine(POSTGRES_CONN)
    df = pd.read_sql("SELECT * FROM bronze_vehicles", engine)

    df.drop_duplicates(inplace=True)

    df.to_sql(
        "silver_vehicles",
        engine,
        if_exists="replace",    # Using 'replace' is OK for now to refresh the table.
        schema="public",        # For incremental/very large datasets, it is better to
        index=False)            # use 'append' or Postgres upsert to avoid rewriting the full table.
    
    logging.info("Silver table 'silver_vehicles' refreshed successfully.")

# Define DAG
with DAG(
    dag_id="etl_vehicles",
    start_date=datetime(2025, 10, 1),
    schedule_interval=None,             # Trigger by etl_master.py
    catchup=False,
    is_paused_upon_creation=False,
) as dag:

    bronze_task = PythonOperator(
        task_id="bronze_load_vehicles",
        python_callable=bronze_load_vehicles,
    )

    silver_task = PythonOperator(
        task_id="silver_transform_vehicles",
        python_callable=silver_transform_vehicles,
    )

    # Bronze must finish before Silver
    bronze_task >> silver_task

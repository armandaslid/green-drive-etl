from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor
import pandas as pd
from sqlalchemy import create_engine

# Create connection to Postgres Database
POSTGRES_CONN = "postgresql+psycopg2://airflow:airflow@postgres:5432/green_drive"

# Aggregate vehicles and emissions into gold
def gold_aggregate():
    engine = create_engine(POSTGRES_CONN)
    
    # Load cleaned silver tables
    vehicles = pd.read_sql("SELECT * FROM silver_vehicles", engine)
    emissions = pd.read_sql("SELECT * FROM silver_emissions", engine)
    
    # Average CO2 and barrels08 per make/year in vehicles
    vehicles_agg = vehicles.groupby(['make','year'])[['co2','barrels08']].mean().reset_index()

    # Average emission scores per vehicle (grouped by vehicle ID)
    # Summarizes multiple emissions records for the same vehicle
    emissions_agg = emissions.groupby('id').agg({
        'score': 'mean',
        'scoreAlt': 'mean',
        'smartwayScore': 'mean'
    }).reset_index()
    
    # Merge unaggregated vehicles and emissions on 'id'
    merged = pd.merge(
        vehicles,
        emissions_agg,
        how='left',
        on='id')
    
    # Aggregate merged table per make/year (keeps vehicles metrics aggregated while adding emissions)
    gold_merged = merged.groupby(['make','year']).agg({
        'co2': 'mean',
        'barrels08': 'mean',
        'score': 'mean',
        'scoreAlt': 'mean',
        'smartwayScore': 'mean'
    }).reset_index()
    
    # Save aggregated tables to Postgres ('replace' for gold tables is standard practice in ETL pipelines)
    with engine.begin() as connection:
        vehicles_agg.to_sql("gold_vehicles_agg", con=connection, if_exists="replace", index=False)
        emissions_agg.to_sql("gold_emissions_agg", con=connection, if_exists="replace", index=False)
        gold_merged.to_sql("gold_vehicles_emissions", con=connection, if_exists="replace", index=False)

# Define DAG
with DAG(
    dag_id="etl_gold",
    start_date=datetime(2025, 10, 1),
    schedule_interval=None,  # Trigger by etl_master.py
    catchup=False,
    is_paused_upon_creation=False,
) as dag:

    gold_task = PythonOperator(
        task_id="gold_aggregate",
        python_callable=gold_aggregate,
    )

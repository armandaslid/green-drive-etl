from datetime import datetime
from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

# Master DAG that orchestrates the daily ETL workflow
# It triggers the following child DAGs in sequence:
# 1. etl_vehicles   -> Bronze + Silver vehicle data processing
# 2. etl_emissions  -> Bronze + Silver emissions data processing
# 3. etl_gold       -> Aggregates silver tables into gold tables

with DAG(
    dag_id="etl_master",
    start_date=datetime(2025, 10, 1),
    schedule_interval="@daily",     # Or cron schedule: "0 0 * * *", run once per day
    catchup=False,
    is_paused_upon_creation=False,
) as dag:

    # Trigger the vehicles ETL DAG and wait until it finishes before moving on
    trigger_vehicles = TriggerDagRunOperator(
        task_id="trigger_vehicles",
        trigger_dag_id="etl_vehicles",
        wait_for_completion=True,       # Ensures dependent DAGs run after completion
        poke_interval=30,               # Checks every 30 seconds for completion
    )

    # Trigger the emissions ETL DAG and wait until it finishes
    trigger_emissions = TriggerDagRunOperator(
        task_id="trigger_emissions",
        trigger_dag_id="etl_emissions",
        wait_for_completion=True,
        poke_interval=30,
    )

    # Trigger the gold aggregation DAG
    # This will only run after both vehicles and emissions DAGs have finished
    trigger_gold = TriggerDagRunOperator(
        task_id="trigger_gold",
        trigger_dag_id="etl_gold",
        wait_for_completion=True,
        poke_interval=30,
    )

    # Gold aggregation runs after vehicles & emissions ETL
    [trigger_vehicles, trigger_emissions] >> trigger_gold

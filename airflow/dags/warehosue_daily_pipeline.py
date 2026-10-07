from datetime import datetime

from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from _dag_helpers import DEFAULT_ARGS, run_script

with DAG(
    dag_id="warehouse_daily_pipeline",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 1, 1),
    schedule="0 2 * * *",
    catchup=False,
    max_active_runs=100,
    tags=["warehouse", "daily"],
) as dag:
    load_dimensions = run_script("load_dimensions", "pipelines", "load_dimensions.py")
    load_fact_transactions = run_script("load_fact_transactions", "pipelines", "load_fact_transactions.py")

    start_quality_checks = TriggerDagRunOperator(
        task_id="start_quality_checks",
        trigger_dag_id="data_quality_pipeline",
        wait_for_completion=False,
    )

    load_dimensions >> load_fact_transactions >> start_quality_checks
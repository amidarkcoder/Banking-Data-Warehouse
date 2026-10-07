from airflow import DAG
from _dag_helpers import DEFAULT_ARGS, run_script
from datetime import datetime

with DAG(
    dag_id = "data_quality_pipeline",
    default_args = {**DEFAULT_ARGS, "retries":0},
    start_date = datetime(2026,10,4),
    max_active_runs = 1,
    tags = ["quality"]
) as dag:
    run_script("run_quality_checks","tests", "test_faker_data.py")

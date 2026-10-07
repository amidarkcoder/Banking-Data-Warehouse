from datetime import datetime

from airflow import DAG
from _dag_helpers import DEFAULT_ARGS, run_script

with DAG(
    dag_id="customer_batch_pipeline",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026,10,4),
    schedule="@hourly",
    catchup=False,
    max_active_runs=10,
    tags=["customer", "batch"],
) as dag:
    consume_customers = run_script("consume_customers", "kafka/consumers", "customer_consumer.py")
    transform_customers = run_script("transform_customers", "pipelines", "transform_customers.py")
    apply_customer_scd3 = run_script("apply_customer_scd3", "pipelines", "apply_customer_scd3.py")

    consume_customers >> transform_customers >> apply_customer_scd3
from datetime import datetime

from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from _dag_helpers import DEFAULT_ARGS, run_script

with DAG(
    dag_id="ingest_pipeline",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 10, 8),
    schedule="@hourly",
    catchup=False,
    max_active_runs=1,
    tags=["ingest", "kafka"],
) as dag:

    

    consume_customers    = run_script("consume_customers",    "kafka/consumers", "customer_consumer.py")
    consume_accounts     = run_script("consume_accounts",     "kafka/consumers", "account_consumer.py")
    consume_transactions = run_script("consume_transactions", "kafka/consumers", "transaction_consumers.py")

    transform_customers    = run_script("transform_customers",    "pipelines", "transform_customers.py")
    transform_accounts     = run_script("transform_accounts",     "pipelines", "transform_account.py")
    transform_transactions = run_script("transform_transactions", "pipelines", "transform_transaction.py")

    apply_scd3 = run_script("apply_customer_scd3", "pipelines", "apply_customer_scd3.py")

    trigger_warehouse = TriggerDagRunOperator(
        task_id="trigger_warehouse",
        trigger_dag_id="warehouse_daily_pipeline",
        wait_for_completion=False,
    )

    consume_customers    >> transform_customers >> apply_scd3
    consume_accounts     >> transform_accounts
    consume_transactions >> transform_transactions
    [apply_scd3, transform_accounts, transform_transactions] >> trigger_warehouse
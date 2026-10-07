from airflow import DAG
from _dag_helpers import DEFAULT_ARGS, run_script
from datetime import datetime

with DAG(
    dag_id = "transaction_stream_pipeline",
    default_args = DEFAULT_ARGS,
    start_date = datetime(2026,10,5),
    schedule = "@hourly",
    catchup = False,
    max_active_runs = 100,
    tags = ["transactions","streaming"]
) as dag :
    consume_account = run_script("consume_accounts","kafka/consumers", "account_consumer.py")
    transform_account = run_script("transform_account","pipelines","transform_account.py")

    consume_transaction = run_script("consume_transaction","kafka/consumers","transaction_consumers.py")
    transform_transaction = run_script("transform_transaction","pipelines","transform_transaction.py")

    consume_account >> transform_account
    consume_transaction >> transform_transaction


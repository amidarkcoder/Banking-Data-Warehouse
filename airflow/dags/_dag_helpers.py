
import os
from datetime import datetime, timedelta

from airflow.operators.bash import BashOperator


PROJECT_ROOT = os.getenv("PROJECT_ROOT", "/opt/airflow/project")
DEFAULT_ARGS = {
    "owner": "data-engineering",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}


def run_script(task_id, folder, script, **kwargs):
    """One task = run one Python script from its own folder.
    Scripts read the DB and Kafka settings from the container's environment variables."""
    return BashOperator(
        task_id=task_id,
        bash_command=f"cd {PROJECT_ROOT}/{folder} && python {script}",
        **kwargs,
    )
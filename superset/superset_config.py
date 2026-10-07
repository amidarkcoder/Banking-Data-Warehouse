import os

SQLALCHEMY_DATABASE_URI = (
    "postgresql+psycopg2://airflow:"
    f"{os.environ['AIRFLOW_DB_PASSWORD']}@airflow-db:5432/superset"
)

SECRET_KEY = os.environ["SUPERSET_SECRET_KEY"]

ROW_LIMIT = 50000
SUPERSET_WEBSERVER_TIMEOUT = 120

FEATURE_FLAGS = {
    "DASHBOARD_CROSS_FILTERS": True,
    "DASHBOARD_NATIVE_FILTERS": True,
}
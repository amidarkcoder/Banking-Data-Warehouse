# Build context is the airflow/ folder (build: ./airflow in docker-compose.yml).
FROM apache/airflow:2.10.5-python3.11

COPY requirements.txt /requirements.txt
# Pinning apache-airflow keeps pip from upgrading Airflow itself.
RUN pip install --no-cache-dir "apache-airflow==${AIRFLOW_VERSION}" -r /requirements.txt
import os

# How much data each run generates
NUM_CUSTOMER     = 1000
NUM_ACCOUNTS     = 1500
NUM_TRANSACTIONS = 5000

# Kafka: Mac = localhost:9092, Airflow sets KAFKA_BOOTSTRAP=kafka:29092
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092")

TOPICS = {
    "customers":    os.getenv("CUSTOMER_TOPIC",    "customer_events"),
    "accounts":     os.getenv("ACCOUNT_TOPIC",     "account_events"),
    "transactions": os.getenv("TRANSACTION_TOPIC", "transaction_events"),
}

# Postgres: Mac = localhost, Airflow sets POSTGRES_HOST=postgres
PG = {
    "host":     os.getenv("POSTGRES_HOST", "localhost"),
    "port":     os.getenv("POSTGRES_PORT", "5432"),
    "dbname":   os.getenv("POSTGRES_DB", "enterprise_dw"),
    "user":     os.getenv("POSTGRES_USER", "postgres"),
    "password": os.getenv("POSTGRES_PASSWORD", ""),
}
import json,os

import psycopg2
from psycopg2.extras import execute_values
from kafka import KafkaConsumer

TOPIC = os.getenv("CUSTOMER_TOPIC", "customer_events")
GROUP_ID = "customer-raw-writer"
TABLE = "raw.customer_events"
COLUMNS = ["event_id", "customer_id", "first_name","last_name","email",
           "phone_number","city","state","country","customer_segment",
           "event_type","event_timestamp"]

INSERT_SQL = f"""
    insert into {TABLE} ({", ".join(COLUMNS)})
    values %s
    on conflict (event_id) do nothing
"""

def main():
    conn = psycopg2.connect(
        host = os.getenv("POSTGRES_HOST","localhost"),
        dbname = os.getenv("POSTGRES_DB","enterprise_dw"),
        user = os.getenv("POSTGRES_USER", "postgres"),
        password = os.getenv("POSTGRES_PASSWORD","")## need to put password
    )

    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP", "localhost:9092"),
        group_id = GROUP_ID,
        enable_auto_commit = False,
        auto_offset_reset = "earliest",
        value_deserializer = lambda b: json.loads(b.decode("utf-8"))
    )

    while True:
        batches = consumer.poll(timeout_ms=5000, max_records=500)
        messages = [m for msgs in batches.values() for m in msgs]
        if not messages:
            break

        rows = [tuple(m.value.get(c) for c in COLUMNS) for m in messages]
        with conn.cursor() as cur:
            execute_values(cur, INSERT_SQL, rows)
        conn.commit()
        consumer.commit()

    conn.close()

if __name__ == "__main__":
    main()

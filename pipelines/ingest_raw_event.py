"""Store every Kafka message unchanged (JSONB) in raw.kafka_events."""

import json
import os
import uuid
from datetime import datetime,timezone
from kafka import KafkaConsumer
from psycopg2.extras import Json
from common import get_connection

topic = [
    os.getenv("CUSTOMER_TOPIC","customer_events"),
    os.getenv("ACCOUNT_TOPIC","account_events"),
    os.getenv("TRANSACTION_TOPIC","transaction_events")
]

insert_sql = """
        insert into raw.kafka_event
            (event_id, event_type, topic_name, partition_number, offset_number,
            event_key,payload,event_timestamp, ingested_at, processing_status)
        values(%s,%s,%s,%s,%s,%s,%s,%s,now(),'NEW')
        on conflict(topic_name,partition_number,offset_number) do nothing
"""

def main():
    conn = get_connection()
    consumer = KafkaConsumer(
        *topic,
        bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP", "localhost:9092"),
        group_id = "raw-ingest",
        enable_auto_commit = False,
        auto_offset_reset="earliest",
        value_deserialize= lambda b: json.loads(b.decode("utf-8")),
        key_deserializer = lambda b: b.decode("utf-8") if b else None,
        consumer_timeout_ms = 10000
    )
    count = 0
    with conn.cursor() as cur:
        for msg in consumer:
            p = msg.value
            cur.exeute(insert_sql,(
                p.get("event_id") or str(uuid.uuid4()),
                p.get("event_type"),
                msg.topic, msg.partition, msg.offset, msg.key,
                Json(p),
                p.get("event_timestamp") or p.get("transaction_timestamp")
                or datetime.now(timezone.utc)
            ))
            conn.commit()
            consumer.commit()
            count += 1
    conn.close()
    print(f"[ingest_raw_events] stored {count} message")

if __name__ == "__main__":
    main()

import json
import sys
import argparse
import random
import signal
import time
import psycopg2

from kafka import KafkaProducer
import config
from faker_account import faker_account
from faker_customer import faker_customer
from faker_transaction import faker_transaction


def load_reference_data():
    """Read real IDs from the tables loaded by database/seeds."""
    conn = psycopg2.connect(**config.PG)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT branch_id::text FROM warehouse.dim_branch")
            branch_ids = [r[0] for r in cur.fetchall()]
            cur.execute("SELECT product_id::text FROM warehouse.dim_product")
            product_ids = [r[0] for r in cur.fetchall()]
            cur.execute("SELECT channel_code FROM warehouse.dim_channel")
            channels = [r[0] for r in cur.fetchall()]
    finally:
        conn.close()

    if not branch_ids or not product_ids:
        raise RuntimeError(
            "warehouse.dim_branch / dim_product are empty. "
            "Load the seeds first: docker compose run --rm db-seed"
        )
    return branch_ids, product_ids, channels


def generate_all():
    branch_ids, product_ids, channels = load_reference_data()
    branches = [{"branch_id": b} for b in branch_ids]
    products = [{"product_id": p} for p in product_ids]

    customers    = [faker_customer() for _ in range(config.NUM_CUSTOMER)]
    accounts     = faker_account(customers, products, branches, config.NUM_ACCOUNTS)
    transactions = faker_transaction(accounts, config.NUM_TRANSACTIONS, channels)

    return {
        "branches":     branches,
        "products":     products,
        "customers":    customers,
        "accounts":     accounts,
        "transactions": transactions,
    }


def publish(data):
    producer = KafkaProducer(
        bootstrap_servers=config.KAFKA_BOOTSTRAP,
        key_serializer=lambda k: k.encode("utf-8") if k else None,
        value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
        acks="all",
    )

    for name, key_field in [
        ("customers",    "customer_id"),
        ("accounts",     "account_id"),
        ("transactions", "account_id"),
    ]:
        topic = config.TOPICS[name]
        for row in data[name]:
            producer.send(topic, key=row.get(key_field), value=row)
        producer.flush()
        print(f"Published {len(data[name])} rows -> '{topic}'")

    producer.close()



_running = True


def _stop(signum, frame):
    global _running
    _running = False
    print("\nShutdown signal received, flushing...")


def stream(rate):
    """Continuously emit transactions referencing a live pool of accounts."""
    signal.signal(signal.SIGINT, _stop)
    signal.signal(signal.SIGTERM, _stop)

    producer = KafkaProducer(
        bootstrap_servers=config.KAFKA_BOOTSTRAP,
        key_serializer=lambda k: k.encode("utf-8") if k else None,
        value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
        acks="all",
    )

    data = generate_all()
    for name, key in [("customers", "customer_id"), ("accounts", "account_id")]:
        for row in data[name]:
            producer.send(config.TOPICS[name], key=row[key], value=row)
        producer.flush()
        print(f"Seeded {len(data[name])} {name}")

    accounts = data["accounts"]
    _, _, channels = load_reference_data()
    interval = 1.0 / rate
    sent = 0

    print(f"Streaming ~{rate} txn/sec. Ctrl-C to stop.")
    while _running:
        txn = faker_transaction(accounts, 1, channels)[0]
        producer.send(config.TOPICS["transactions"],
                      key=txn["account_id"], value=txn)
        sent += 1
        if sent % 100 == 0:
            producer.flush()
            print(f"  sent {sent} transactions")
        time.sleep(interval)

    producer.flush()
    producer.close()
    print(f"Stopped after {sent} transactions")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--stream", action="store_true", help="run continuously")
    ap.add_argument("--rate", type=float, default=5.0, help="transactions per second")
    ap.add_argument("--dry-run", action="store_true", help="generate only, no publish")
    args = ap.parse_args()

    if args.stream:
        stream(args.rate)
    else:
        data = generate_all()
        for name, rows in data.items():
            print(f"{name}: {len(rows)} rows")
        if not args.dry_run:
            publish(data)
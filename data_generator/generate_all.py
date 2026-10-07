"""
Generate fake banking events and publish them to Kafka.

- Reference data (branches, products, channels) is read from the seeded
  warehouse.dim_* tables, so every event links to a real row.
- Event data (customers, accounts, transactions) is faked and published.

Usage:
    python generate_all.py            # generate + publish to Kafka
    python generate_all.py --dry-run  # generate only, print counts
"""
import json
import sys

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

    # Order matters: customers before accounts before transactions.
    # The message key keeps all events of one entity in the same partition, in order.
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


if __name__ == "__main__":
    data = generate_all()
    for name, rows in data.items():
        print(f"{name}: {len(rows)} rows")

    if "--dry-run" not in sys.argv:
        publish(data)
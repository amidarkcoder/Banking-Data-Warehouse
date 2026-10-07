import random
import uuid
from datetime import datetime, timedelta

from faker import Faker

fake = Faker()

STATUSES = ["active", "active", "active", "dormant", "closed"]  # mostly active


def faker_account(customers, products, branches, n):
    """Generate n accounts that reference REAL customers, products, and branches."""
    customer_ids = [c["customer_id"] for c in customers]
    product_ids  = [p["product_id"]  for p in products]
    branch_ids   = [b["branch_id"]   for b in branches]

    accounts = []
    for _ in range(n):
        status       = random.choice(STATUSES)
        opening_date = fake.date_between(start_date="-5y", end_date="-30d")
        closing_date = (
            fake.date_between(start_date=opening_date, end_date="today")
            if status == "closed" else None
        )
        event_ts = fake.date_time_between(start_date=opening_date, end_date="now")

        accounts.append({
            "event_id":        str(uuid.uuid4()),
            "account_id":      str(uuid.uuid4()),
            "customer_id":     random.choice(customer_ids),
            "product_id":      random.choice(product_ids),
            "branch_id":       random.choice(branch_ids),
            "account_number":  fake.unique.numerify("##########"),
            "account_status":  status,
            "opening_date":    opening_date.isoformat(),
            "closing_date":    closing_date.isoformat() if closing_date else None,
            "event_type":      "ACCOUNT_CLOSED" if status == "closed" else "ACCOUNT_OPENED",
            "event_timestamp": event_ts.isoformat(),
            "ingested_at":     datetime.now().isoformat(),
        })
    return accounts
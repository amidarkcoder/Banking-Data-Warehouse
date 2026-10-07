import random
import uuid
from datetime import datetime

from faker import Faker

fake = Faker()

TXN_TYPES    = ["PAYMENT", "DEPOSIT", "WITHDRAWAL", "TRANSFER", "PURCHASE"]
TXN_STATUSES = ["COMPLETED"] * 8 + ["PENDING", "FAILED"]   # mostly completed
CHANNELS     = ["ONLINE", "MOBILE", "ATM", "BRANCH", "POS"]
CURRENCIES   = ["USD", "EUR", "GBP", "INR"]


def faker_transaction(accounts, n, channels=None):
    """Generate n transactions that reference REAL accounts and channels."""
    channel_list  = channels or CHANNELS
    open_accounts = [a for a in accounts if a["account_status"] != "closed"] or accounts

    transactions = []
    for _ in range(n):
        acc = random.choice(open_accounts)
        txn_date = fake.date_time_between(start_date="-30d", end_date="now")
        transactions.append({
            "event_id":            str(uuid.uuid4()),
            "transaction_id":      str(uuid.uuid4()),
            "account_id":          acc["account_id"],
            "customer_id":         acc["customer_id"],
            "product_id":          acc["product_id"],
            "branch_id":           acc["branch_id"],
            "transaction_type":    random.choice(TXN_TYPES),
            "transaction_status":  random.choice(TXN_STATUSES),
            "transaction_amount":  round(random.uniform(5, 5000), 2),
            "currency_code":       random.choice(CURRENCIES),
            "transaction_timestamp": txn_date.isoformat(),
            "merchant_name": fake.name(),
            "channel":             random.choice(channel_list),
            "ingestion_timestamp": datetime.now().isoformat(),
        })
    return transactions
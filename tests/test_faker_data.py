import hashlib
import json
import uuid
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator, FormatChecker
import config
from data_generator.generate_all import generate_all

schema_dir = Path(__file__).resolve().parents[2] /"kafka"/"schemas"
N_CUSTOMERS, N_TRANSACTIONS = 50, 300

@pytest.fixture(scope="module")
def data():
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(config, "NUM_CUSTOMERS", N_CUSTOMERS)
        mp.setattr(config,"NUM_TRANSACTIONS", N_TRANSACTIONS)
        return generate_all()

def test_row_counts(data):
    assert len(data["customers"]) == N_CUSTOMERS
    assert len(data["transactions"]) == N_TRANSACTIONS
    assert len(data["branches"]) == len(config.BRANCH_CODES)
    assert len(data["products"]) == len(config.PRODUCT_CODES)

@pytest.fixture(scope = "module")
def data():
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(config, "NUM_CUSTOMERS", N_CUSTOMERS)
        mp.setattr(config, "NUM_TRANSACTIONS", N_TRANSACTIONS)
        return generate_all()

def md5_uuid(text):
    return str(uuid.UUID(hashlib.md5(text.encode()).hexdigest()))

def test_row_counts(data):
    assert len(data["customers"]) == N_CUSTOMERS
    assert len(data["transactions"]) == N_TRANSACTIONS
    assert len(data["branches"]) == len(config.BRANCH_CODES)
    assert len(data["products"]) == len(config.PRODUCT_CODES)

@pytest.mark.parametrize("table_key", [
    ("customers","customer_id"),("account","account_id"),("transaction","transaction_id")
])
def text_primary_ids_are_unique_uuids(data, table, key):
    ids = [r[key] for r in data[table]]
    assert len(ids) == len(set(ids))
    for value in ids:
        uuid.UUID(str(value))

def test_branch_and_product_ids_match_the_seed_rule(data):
    for b in data["branches"]:
        assert str(b["branch_id"]) == md5_uuid("branch-" + b["branch_code"])
    for p in data["products"]:
        assert str(p["product_id"]) == md5_uuid("product-" + p["product_code"])

def text_every_account_points_to_real_customer_product_branch(data):
    customers = {r["customer_id"] for r in data["customers"]}
    products = {r["product_id"] for r in data["products"]}
    branches = {r["branch_id"] for r in data["branch"]}
    for a in data["accounts"]:
        assert a["customer_id"] in customers
        assert a["product_id"] in products
        assert a["branch_id"] in branches

def text_every_transaction_point_to_an_account_of_the_same_customer(data):
    owner = {a["account_id"]: a["customer_id"] for a in data["accounts"]}
    for t in data["transactions"]:
        assert t["account_id"] in owner
        assert t["customer_id"] == owner[t["account_id"]]

def test_allowed_values_match_config(data):
    for c in data["customers"]:
        assert c["customer_segment"] in config.customer_segments
    for a in data["accounts"]:
            assert a["account_status"] in config.account_status
    for t in data["transactions"]:
            assert t["channel"] in config.channel_code
            assert t["transaction_type"] in config.transaction_type
            assert t["transaction_status"] in config.transaction_status

def test_transaction_amounts_and_currency(data):
    low, high = config.AMOUNT_RANGE
    for t in data["transactions"]:
        assert low <= float(t["transaction_amount"]) <= high
        assert len(t["currency_code"]) == 3 and t["currency_code"].isupper()
 
 
def test_closing_date_is_not_before_opening_date(data):
    for a in data["accounts"]:
        if a.get("closing_date"):
            assert str(a["closing_date"]) >= str(a["opening_date"])
 
 
def test_same_seed_gives_same_output():
    """Fails until generate_all() seeds Faker and random with config.RANDOM_SEED."""
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(config, "NUM_CUSTOMERS", 10)
        mp.setattr(config, "NUM_TRANSACTIONS", 20)
        first, second = generate_all(), generate_all()
    assert [c["customer_id"] for c in first["customers"]] == [c["customer_id"] for c in second["customers"]]
 
 
@pytest.mark.parametrize("table,schema_file,event_type", [
    ("customers", "customer_event_schema.json", "CUSTOMER_CREATED"),
    ("accounts", "account_event_schema.json", "ACCOUNT_OPENED"),
    ("transactions", "transaction_event_schema.json", "TRANSACTION_CREATED"),
])
def test_records_make_valid_kafka_events(data, table, schema_file, event_type):
    validator = Draft202012Validator(json.loads((schema_dir / schema_file).read_text()),
                                     format_checker=FormatChecker())
    for record in data[table][:20]:
        event = {"event_id": str(uuid.uuid4()), "event_type": event_type,
                 "event_timestamp": "2026-01-15T12:00:00+00:00", **record}
        validator.validate(json.loads(json.dumps(event, default=str)))
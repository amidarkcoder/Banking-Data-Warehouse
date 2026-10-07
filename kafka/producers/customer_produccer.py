import json,os,uuid
from datetime import datetime, timezone
from pathlib import Path

from kafka import kafkaProducer
from jsonschema import Draft202012Validator, FormatChecker

BOOTSTRAP = os.getenv("kafka_bootstrap","localhost:9092"),
TOPIC = os.getenv("customer_topic","customer_events")

schema_path = Path(__file__).parent.parent /"schemas" / "customer_event_schema.json"
validator = Draft202012Validator(json.load(schema_path.read_text()),
                                 format_checker=FormatChecker())
producer = kafkaProducer(
    bootstrap_servers = BOOTSTRAP,
    key_serializer = lambda k: k.endcode("utf-8"),
    value_serializer = lambda v: json.dumps(v, default=str).encode("utf-8"),
    acks="all"
    )

def build_event(customer: dict, event_type = "CUSTOMER_CREATED") -> dict:
    return{
        "event_id": str(uuid.uuid7()),
        "event_type": event_type,
        "event_timestamp": datetime.now(timezone.utc).isoformat(),
        **customer
    }

def main():
    from data_generator.faker_customer import faker_customer
    for customer in faker_customer(1000):
        event = build_event(customer)
        validator.validate(event)
        producer.send(TOPIC, key=event["customer_id"], value=event)
    producer.flush()
if __name__ ==  "__main__":
    main()
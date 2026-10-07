"""raw.customer_events -> staging.stg_customer"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from common import run_step

if __name__ == "__main__":
    run_step("transform_customer", ["staging/stg_customer.sql"])
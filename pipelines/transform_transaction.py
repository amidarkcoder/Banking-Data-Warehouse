"""raw.transaction_event -> staging.stg_transaction"""

from common import run_step

if __name__ == "__main__":
    run_step("transform_transaction", ["staging/stg_transaction.sql"])
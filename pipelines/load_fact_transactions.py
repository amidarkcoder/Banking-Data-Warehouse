"""staging.stg_transaction + all dimesnsions -> warehouse.fact_transactions"""
import os
from common import run_step

if __name__ == "__main__":
    run_step(
        "load_fact_transactions",
        ["warehouse/fact_transactions.sql"],
        params ={
            "fee_rate": os.getenv("fee_rate", "0.00"),
            "tax_rate": os.getenv("tax_rate","0.00")
            }
)
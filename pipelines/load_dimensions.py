"""Load dim_date and dim_account.
dim_product / dim_branch / dim_channel come from database/seeds, not from here.
Run apply_customer_scd3.py BEFORE this script(dim_account needs customer_key)."""

from common import run_step

if __name__ == "__main__":
    run_step("load_dimensions",["warehouse/dim_date.sql",
                                "warehouse/dim_account.sql"])

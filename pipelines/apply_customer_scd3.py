"""staging.stg_customer -> warehouse.dim_customer_scd3 (SCD Type 3)"""

from common import run_step

if __name__ == "__main__":
    run_step("apply_customer_scd3", ["warehouse/dim_customer_scd3.sql"])
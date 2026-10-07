"""raw.account_event ->  staging.stg_account"""
from common import run_step

if __name__ == "__main__":
    run_step("transform_account",["staging/stg_account.sql"])
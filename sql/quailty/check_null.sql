SELECT 'null_channel_key' AS check_name, 'warehouse.fact_transactions' AS table_name, count(*) AS failed_rows
FROM warehouse.fact_transactions WHERE channel_key IS NULL
UNION ALL
SELECT 'null_product_key', 'warehouse.fact_transactions', count(*)
FROM warehouse.fact_transactions WHERE product_key IS NULL
UNION ALL
SELECT 'null_branch_key', 'warehouse.fact_transactions', count(*)
FROM warehouse.fact_transactions WHERE branch_key IS NULL
UNION ALL
SELECT 'null_amount_or_net', 'warehouse.fact_transactions', count(*)
FROM warehouse.fact_transactions WHERE transaction_amount IS NULL OR net_amount IS NULL
UNION ALL
SELECT 'null_currency_code', 'warehouse.fact_transactions', count(*)
FROM warehouse.fact_transactions WHERE currency_code IS NULL
UNION ALL
SELECT 'null_product_or_branch_key', 'warehouse.dim_account', count(*)
FROM warehouse.dim_account WHERE product_key IS NULL OR branch_key IS NULL
UNION ALL
SELECT 'null_opening_date_key', 'warehouse.dim_account', count(*)
FROM warehouse.dim_account WHERE opening_date_key IS NULL
UNION ALL
SELECT 'null_email', 'warehouse.dim_customer_scd3', count(*)
FROM warehouse.dim_customer_scd3 WHERE email IS NULL
UNION ALL
SELECT 'null_customer_segment', 'warehouse.dim_customer_scd3', count(*)
FROM warehouse.dim_customer_scd3 WHERE customer_segment IS NULL
UNION ALL
SELECT 'null_email', 'staging.stg_customer', count(*)
FROM staging.stg_customer WHERE email IS NULL
UNION ALL
SELECT 'null_account_status', 'staging.stg_account', count(*)
FROM staging.stg_account WHERE account_status IS NULL
UNION ALL
SELECT 'null_amount_or_timestamp', 'staging.stg_transaction', count(*)
FROM staging.stg_transaction WHERE transaction_amount IS NULL OR transaction_timestamp IS NULL;
INSERT INTO warehouse.fact_transactions (
    transaction_id, account_key, customer_key, product_key, branch_key,
    transaction_type, transaction_status, transaction_amount, 
    fee_amount, tax_amount, net_amount, currency_code, 
    merchant_name, transaction_timestamp, date_key, loaded_at
)
SELECT 
    s.transaction_id,
    COALESCE(a.account_key, -1) AS account_key,
    COALESCE(a.customer_key, -1) AS customer_key,
    COALESCE(p.product_key, -1) AS product_key,
    COALESCE(b.branch_key, -1) AS branch_key,
    s.transaction_type,
    s.transaction_status,
    s.transaction_amount,
    COALESCE(s.fee_amount, (s.transaction_amount * %(fee_rate)s::NUMERIC)) AS fee_amount,
    COALESCE(s.tax_amount, (s.transaction_amount * %(tax_rate)s::NUMERIC)) AS tax_amount,
    COALESCE(s.net_amount, s.transaction_amount) AS net_amount,
    s.currency_code,
    s.merchant_name,
    s.transaction_timestamp,
    TO_CHAR(s.transaction_timestamp, 'YYYYMMDD')::INT AS date_key,
    NOW() AS loaded_at
FROM staging.stg_transaction s
LEFT JOIN warehouse.dim_account a ON a.account_id = s.account_id
LEFT JOIN warehouse.dim_product p ON p.product_id = s.product_id
LEFT JOIN warehouse.dim_branch b   ON b.branch_id = s.branch_id
ON CONFLICT (transaction_id) DO UPDATE SET
    account_key           = EXCLUDED.account_key,
    customer_key          = EXCLUDED.customer_key,
    product_key           = EXCLUDED.product_key,
    branch_key            = EXCLUDED.branch_key,
    transaction_type      = EXCLUDED.transaction_type,
    transaction_status    = EXCLUDED.transaction_status,
    transaction_amount    = EXCLUDED.transaction_amount,
    fee_amount            = EXCLUDED.fee_amount,
    tax_amount            = EXCLUDED.tax_amount,
    net_amount            = EXCLUDED.net_amount,
    currency_code         = EXCLUDED.currency_code,
    merchant_name         = EXCLUDED.merchant_name,
    transaction_timestamp = EXCLUDED.transaction_timestamp,
    date_key              = EXCLUDED.date_key,
    loaded_at            = NOW()
WHERE (warehouse.fact_transactions.transaction_status, warehouse.fact_transactions.transaction_amount) 
      IS DISTINCT FROM 
      (EXCLUDED.transaction_status, EXCLUDED.transaction_amount);

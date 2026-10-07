TRUNCATE TABLE staging.stg_transaction;

INSERT INTO staging.stg_transaction (
    transaction_id, account_id, customer_id, product_id, branch_id,
    transaction_type, transaction_status, transaction_amount,
    fee_amount, tax_amount, net_amount,
    currency_code, transaction_timestamp, merchant_name, channel,
    record_hash, load_date
)
SELECT
    nullif(transaction_id::text, '')::uuid,
    nullif(account_id::text,     '')::uuid,
    nullif(customer_id::text,    '')::uuid,
    nullif(product_id::text,     '')::uuid,
    nullif(branch_id::text,      '')::uuid,
    INITCAP(TRIM(transaction_type)),
    INITCAP(TRIM(transaction_status)),
    transaction_amount::numeric,
    NULL::numeric,
    NULL::numeric,
    NULL::numeric,
    currency_code,
    nullif(transaction_timestamp::text, '')::timestamp,
    TRIM(merchant_name),
    INITCAP(TRIM(channel)),
    ENCODE(SHA256(convert_to(CONCAT_WS('|',
        TRIM(transaction_id::TEXT),
        TRIM(account_id::TEXT),
        TRIM(customer_id::TEXT),
        TRIM(product_id::TEXT),
        TRIM(branch_id::TEXT),
        INITCAP(TRIM(transaction_type)),
        INITCAP(TRIM(transaction_status)),
        transaction_amount,
        TRIM(merchant_name),
        INITCAP(TRIM(channel))
    ), 'UTF8')), 'hex'),
    CURRENT_DATE
FROM (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY transaction_id
               ORDER BY transaction_timestamp DESC, loaded_at DESC
           ) AS rn
    FROM raw.transaction_events
    WHERE transaction_id IS NOT NULL
      AND transaction_amount IS NOT NULL
      AND transaction_timestamp IS NOT NULL
) e
WHERE rn = 1;
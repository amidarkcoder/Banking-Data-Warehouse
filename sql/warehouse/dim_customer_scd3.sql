    INSERT INTO warehouse.dim_customer_scd3 AS d (
        customer_id, first_name, last_name, email, phone_number, 
        city, state, customer_segment, first_seen_at,
        last_updated_at, record_hash, is_active
    )
SELECT 
    customer_id, first_name, last_name, email, phone_number, 
    city, state, customer_segment, NOW(), source_updated_at,
    record_hash, -- Use the SHA-256 hash calculated in staging
    TRUE
FROM staging.stg_customer

    ON CONFLICT (customer_id) DO UPDATE SET
        -- Fixed: Added missing "FROM" keyword to IS DISTINCT FROM clauses
        previous_email = CASE 
            WHEN d.email IS DISTINCT FROM EXCLUDED.email THEN d.email 
            ELSE d.previous_email 
        END,
        previous_customer_segment = CASE 
            WHEN d.customer_segment IS DISTINCT FROM EXCLUDED.customer_segment THEN d.customer_segment 
            ELSE d.previous_customer_segment 
        END,
        email = EXCLUDED.email,
        customer_segment = EXCLUDED.customer_segment,
        last_updated_at = NOW(),
        record_hash = EXCLUDED.record_hash
    -- Fixed: Explicitly referencing EXCLUDED table for validation
    WHERE d.record_hash <> EXCLUDED.record_hash;

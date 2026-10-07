truncate staging.stg_account;

insert into staging.stg_account
    (account_id, customer_id, product_id, branch_id, account_number,
     account_status, opening_date, closing_date, record_hash, load_date)
select
    nullif(account_id::text,  '')::uuid,
    nullif(customer_id::text, '')::uuid,
    nullif(product_id::text,  '')::uuid,
    nullif(branch_id::text,   '')::uuid,
    trim(account_number),
    initcap(trim(account_status)),
    nullif(opening_date::text, '')::date,
    nullif(closing_date::text, '')::date,
    encode(sha256(convert_to(concat_ws('|',
        account_id::text,
        customer_id::text,
        product_id::text,
        branch_id::text,
        trim(account_number)
    ), 'UTF8')), 'hex'),
    current_date
from (
    select *,
           row_number() over (
               partition by account_id
               order by event_timestamp desc, ingested_at desc
           ) as rn
    from raw.account_event
    where account_id is not null
) e
where rn = 1;
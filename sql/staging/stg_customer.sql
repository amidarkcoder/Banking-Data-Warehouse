truncate staging.stg_customer;

insert into staging.stg_customer
(customer_id, first_name, last_name, email, phone_number, city, state, country, customer_segment, source_updated_at, record_hash, load_date)
select
    customer_id,
    initcap(trim(first_name)),
    initcap(trim(last_name)),
    lower(trim(email)),
    trim(phone_number),
    trim(city),
    trim(state),
    trim(country),
    initcap(trim(customer_segment)),
    event_timestamp,
    -- Replace the inner hash block with this to match your transformation:
    encode(
        sha256(
            concat_ws('|', 
                initcap(trim(customer_id::text)), 
                initcap(trim(first_name)), 
                initcap(trim(last_name)), 
                lower(trim(email)), 
                trim(phone_number), 
                trim(city), 
                trim(state), 
                trim(country), 
                initcap(trim(customer_segment))
            )::bytea
        ), 
        'hex'
    ),
    current_date
from (select *,
          row_number() over (partition by customer_id order by event_timestamp desc, ingested_at desc) as rn
        from raw.customer_events
        where customer_id is not null
) e
where rn = 1;
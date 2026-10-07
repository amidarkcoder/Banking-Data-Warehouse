insert into warehouse.dim_account as d
    (account_id, account_number, customer_key, product_key, branch_key,
     account_status, opening_date_key, closing_date_key, created_at, updated_at, is_active)
select
    s.account_id, s.account_number, c.customer_key, p.product_key, b.branch_key,
    s.account_status,
    to_char(s.opening_date, 'YYYYMMDD')::int,
    to_char(s.closing_date, 'YYYYMMDD')::int,
    now(), now(),
    (s.account_status is not distinct from 'ACTIVE')
from staging.stg_account s
join      warehouse.dim_customer_scd3 c on c.customer_id = s.customer_id
left join warehouse.dim_product       p on p.product_id  = s.product_id
left join warehouse.dim_branch        b on b.branch_id   = s.branch_id
on conflict (account_id) do update set
    account_number   = excluded.account_number,
    customer_key     = excluded.customer_key,
    product_key      = excluded.product_key,
    branch_key       = excluded.branch_key,
    account_status   = excluded.account_status,
    opening_date_key = excluded.opening_date_key,
    closing_date_key = excluded.closing_date_key,
    is_active        = excluded.is_active,
    updated_at       = now()
where (d.account_number, d.customer_key, d.product_key, d.branch_key,
       d.account_status, d.opening_date_key, d.closing_date_key, d.is_active)
      is distinct from
      (excluded.account_number, excluded.customer_key, excluded.product_key, excluded.branch_key,
       excluded.account_status, excluded.opening_date_key, excluded.closing_date_key, excluded.is_active);
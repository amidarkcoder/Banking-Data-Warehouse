create table if not exists warehouse.fact_transactions(
    transaction_key bigserial primary key,
    transaction_id uuid not null,
    date_key integer references warehouse.dim_date (date_key),
    customer_key bigint references warehouse.dim_customer_scd3 (customer_key),
    account_key bigint references warehouse.dim_account (account_key),
    product_key bigint references warehouse.dim_product (product_key),
    branch_key bigint  references warehouse.dim_branch (branch_key),
    channel_key bigint references warehouse.dim_channel (channel_key),
    transaction_type varchar(50),
    transaction_status varchar(50),
    transaction_amount numeric(18,2),
    fee_amount numeric(18,2),
    tax_amount numeric(18,2),
    net_amount numeric(18,2),
    currency_code char(3),
    merchant_name varchar(225),
    transaction_timestamp timestamp,
    loaded_at timestamp default now()
);
create index if not exists idx_fact_tnx_fact_date on warehouse.fact_transactions (date_key);
create index if not exists idx_fact_tnx_fact_customer on warehouse.fact_transactions (customer_key);
create index if not exists idx_fact_tnx_fact_account on warehouse.fact_transactions (account_key);

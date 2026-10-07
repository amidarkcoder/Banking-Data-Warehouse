create table if not exists staging.stg_customer(
    customer_id uuid primary key,
    first_name varchar(100),
    last_name varchar(100),
    email varchar(225),
    phone_number varchar(30),
    city varchar(100),
    state varchar(100),
    country varchar(100),
    customer_segment varchar(50),
    source_updated_at timestamp,
    record_hash  varchar(64),
    load_date date not null default current_date
);

create table if not exists staging.stg_account(
    account_id uuid primary key,
    customer_id uuid not null,
    product_id uuid,
    branch_id uuid,
    account_number varchar(30),
    account_status varchar(30),
    opening_date date,
    closing_date date,
    record_hash varchar(64),
    load_date date not null default current_date
);

create table if not exists staging.stg_transaction(
    transaction_id uuid primary key,
    account_id uuid not null,
    customer_id uuid not null,
    product_id uuid,
    branch_id uuid,
    transaction_type varchar(50),
    transaction_status varchar(50),
    transaction_amount numeric(18,2),
    currency_code char(3),
    transaction_timestamp timestamp,
    merchant_name varchar(255),
    channel varchar(50),
    record_hash varchar(64),
    load_date date not null default current_date
);
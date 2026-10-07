create table if not exists warehouse.dim_date(
    date_key integer primary key,
    full_date date,
    day_of_month integer,
    day_name varchar(20),
    week_number integer,
    month_number integer,
    month_name varchar(20),
    quarter_number integer,
    year integer,
    is_weekend boolean,
    is_month_end boolean
);

create table if not exists warehouse.dim_customer_scd3(
    customer_key bigserial primary key,
    customer_id uuid not null unique,
    first_name varchar(50),
    last_name varchar(50),
    email varchar(255),
    previous_email varchar(255),
    phone_number varchar(50),
    previous_phone_number varchar(50),
    city varchar(50),
    previous_city varchar(50),
    state varchar(50),
    previous_state varchar(50),
    customer_segment varchar(50),
    previous_customer_segment varchar(50),
    first_seen_at timestamp not null default now(),
    last_updated_at timestamp not null default now(),
    record_hash varchar(64),
    is_active boolean not null default true
);

create table if not exists warehouse.dim_product(
    product_key bigserial primary key,
    product_id uuid not null unique,
    product_code varchar(50) not null unique,
    product_name varchar(150),
    product_category varchar(100),
    interst_rate numeric(8,4),
    monthly_fee numeric(12,2),
    is_active boolean not null default true,
    created_at timestamp not null default now(),
    updated_at timestamp not null default now()
);

create table if not exists warehouse.dim_branch(
    branch_key bigserial primary key,
    branch_id uuid not null unique,
    branch_code varchar(30) not null unique,
    branch_name varchar(150),
    city varchar(50),
    state varchar(50),
    country varchar(50),
    region varchar(50),
    branch_type varchar(50),
    is_active boolean not null default true
);

create table if not exists warehouse.dim_channel(
    channel_key bigserial primary key,
    channel_code varchar(50),
    channel_name varchar(100),
    channel_group varchar(50)
);

create table if not exists warehouse.dim_account(
    account_key bigserial primary key,
    account_id uuid not null,
    account_number varchar(30),
    customer_key bigint REFERENCES warehouse.dim_customer_scd3 (customer_key),
    product_key bigint REFERENCES warehouse.dim_product (product_key),
    branch_key bigint REFERENCES warehouse.dim_branch (branch_key),
    account_status varchar(30),
    opening_date_key integer references warehouse.dim_date (date_key),
    closing_date_key integer references warehouse.dim_date (date_key),
    create_at timestamp not null default now(),
    updated_at timestamp not null default now(),
    is_active boolean not null default true
);






























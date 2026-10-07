create table if not exists raw.kafka_events (
    event_id uuid primary key,
    event_type varchar(50) ,
    topic_name varchar(100) not null,
    partition_number int not null,
    offset_number bigint not null,
    event_key varchar(200),
    payload JSONB not null,
    event_timestamp timestamp,
    ingested_at timestamp not null default now(),
    processing_status varchar(30) not null default 'NEW'
        check (processing_status in('NEW','PROCESS','FAILED')),
    error_message text
);
create index if not exists idx_kafka_event_status on raw.kafka_events(processing_status);
CREATE INDEX IF NOT EXISTS idx_kafka_event_status_new ON raw.kafka_events(processing_status) 
WHERE processing_status = 'NEW';

create table if not exists raw.customer_events(
    event_id uuid primary key,
    customer_id uuid not null,
    first_name varchar(100),
    last_name varchar(100),
    email varchar(250),
    phone_number varchar(30),
    city varchar(100),
    state varchar(100),
    country varchar(100),
    customer_segment varchar(100),
    event_type varchar(100),
    event_timestamp timestamp,
    ingested_at timestamp not null default now()
);

create table if not exists raw.account_event(
    event_id uuid primary key,
    account_id uuid not null unique,
    customer_id uuid not null,
    product_id uuid,
    branch_id uuid,
    account_number varchar(50),
    account_status varchar(50),
    opening_date date,
    closing_date date,
    created_at date,
    event_type varchar(50),
    event_timestamp timestamp,
    ingested_at timestamp not null default now()
);

create table if not exists raw.transaction_events(
    event_id uuid primary key,
    transaction_id uuid not null unique,
    account_id uuid not null,
    customer_id uuid not null,
    product_id uuid,
    branch_id uuid,
    transaction_type varchar(64),
    transaction_status varchar(30),
    transaction_amount numeric(18,2),
    fee_amount numeric(18,2),
    tax_amount numeric(18,2),
    net_amount numeric(18,2),
    currency_code char(3),
    merchant_name varchar(50),
    transaction_timestamp timestamp,
    loaded_at timestamp not null default now()
);


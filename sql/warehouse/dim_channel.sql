create table if not exists warehouse.dim_channel (
    channel_key   bigserial    primary key,
    channel_code  varchar(50)  not null unique,
    channel_name  varchar(100) not null,
    channel_group varchar(50),
    is_active     boolean      not null default true,
    created_at    timestamp    not null default now(),
    updated_at    timestamp    not null default now()
);
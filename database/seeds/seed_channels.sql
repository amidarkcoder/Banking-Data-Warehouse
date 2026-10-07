insert into warehouse.dim_channel (channel_code, channel_name, channel_group)
values ('ONLINE', 'Internet Banking',      'Digital'),
       ('MOBILE', 'Mobile Banking App',    'Digital'),
       ('ATM',    'ATM',                   'Self-Service'),
       ('BRANCH', 'Branch Counter',        'In-Person'),
       ('POS',    'Point of Sale Terminal','Card'),
       ('PHONE',  'Phone Banking',         'Assisted')
on conflict (channel_code) do update set
    channel_name  = excluded.channel_name,
    channel_group = excluded.channel_group
where (warehouse.dim_channel.channel_name,
       warehouse.dim_channel.channel_group)
      is distinct from
      (excluded.channel_name, excluded.channel_group);
insert into warehouse.dim_date
    (date_key, full_date, day_of_month, day_name, week_number, month_number,
     month_name, quarter_number, year, is_weekend, is_month_end)
select
    to_char(d, 'YYYYMMDD')::int,
    d::date,
    extract(day     from d)::int,
    to_char(d, 'FMDay'),
    extract(week    from d)::int,
    extract(month   from d)::int,
    to_char(d, 'FMMonth'),
    extract(quarter from d)::int,
    extract(year    from d)::int,
    extract(isodow  from d) in (6, 7),
    d::date = (date_trunc('month', d) + interval '1 month - 1 day')::date
from generate_series('2000-01-01'::date, '2030-12-31'::date, interval '1 day') as d
on conflict (date_key) do nothing;
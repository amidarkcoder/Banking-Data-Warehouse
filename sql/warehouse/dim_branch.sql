insert into warehouse.dim_branch as d
                (branch_id, branch_code, branch_name, city, state, country, region, branch_type, is_active)

values
    (%(branch_id)s, %(branch_code)s, %(branch_name)s, %(city)s, %(state)s, %(country)s, %(region)s, %(branch_type)s, 
    %(is_active)s)
on conflict(branch_id) do update set
    branch_code = excluded.branch_code,
    branch_name = excluded.branch_name,
    city = excluded.city,
    state = excluded.state,
    country = excluded.country,
    region = excluded.region,
    branch_type = excluded.branch_type,
    is_active = excluded.is_active
where(d.branch_code, d.branch_name, d.city, d.state, d.country, d.region, d.branch_type, d.is_active)
    is distinct from 
    (excluded.branch_code, excluded.branch_name, excluded.city, excluded.state, excluded.country, 
    excluded.region, excluded.branch_type, excluded.is_active);
INSERT INTO warehouse.dim_branch
    (branch_id, branch_code, branch_name, city, state, country, region, branch_type, is_active)
SELECT
    md5('branch-' || v.code)::uuid,v.code,v.city || ' Main Branch',v.city, v.state, v.country, v.region,
    'Main',TRUE
FROM (VALUES
    ('BR-00001', 'Tokyo',         'Tokyo',           'Japan',          'Asia Pacific'),
    ('BR-00002', 'London',        'England',         'United Kingdom', 'Europe'),
    ('BR-00003', 'New York City', 'New York',        'United States',  'North America'),
    ('BR-00004', 'Paris',         'Île-de-France',   'France',         'Europe'),
    ('BR-00005', 'Mumbai',        'Maharashtra',     'India',          'Asia Pacific'),
    ('BR-00006', 'Sydney',        'New South Wales', 'Australia',      'Asia Pacific'),
    ('BR-00007', 'Cairo',         'Cairo',           'Egypt',          'Middle East & Africa'),
    ('BR-00008', 'São Paulo',     'São Paulo',       'Brazil',         'Latin America'),
    ('BR-00009', 'Toronto',       'Ontario',         'Canada',         'North America'),
    ('BR-00010', 'Singapore',     'Singapore',       'Singapore',      'Asia Pacific'),
    ('BR-00011', 'Rome',          'Lazio',           'Italy',          'Europe'),
    ('BR-00012', 'Los Angeles',   'California',      'United States',  'North America'),
    ('BR-00013', 'Berlin',        'Berlin',          'Germany',        'Europe'),
    ('BR-00014', 'Seoul',         'Seoul',           'South Korea',    'Asia Pacific'),
    ('BR-00015', 'Bangkok',       'Bangkok',         'Thailand',       'Asia Pacific'),
    ('BR-00016', 'Mexico City',   'Mexico City',     'Mexico',         'Latin America'),
    ('BR-00017', 'Buenos Aires',  'Buenos Aires',    'Argentina',      'Latin America'),
    ('BR-00018', 'Amsterdam',     'Noord-Holland',   'Netherlands',    'Europe'),
    ('BR-00019', 'Cape Town',     'Western Cape',    'South Africa',   'Middle East & Africa')
) AS v(code, city, state, country, region)
ON CONFLICT (branch_id) DO UPDATE SET
    branch_name = EXCLUDED.branch_name,
    city        = EXCLUDED.city,
    state       = EXCLUDED.state,
    country     = EXCLUDED.country,
    region      = EXCLUDED.region;
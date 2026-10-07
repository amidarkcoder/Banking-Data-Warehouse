insert into warehouse.dim_product
    (product_id, product_code, product_name, product_category, interest_rate, monthly_fee, is_active)
select md5('product-' || code)::uuid, code, name, category, rate, fee, true
from (
    values
    ('SAV-001', 'Basic Savings Account',      'Savings',     0.0150,   0.00),
    ('SAV-002', 'Premium Savings Account',    'Savings',     0.0200,   0.00),
    ('CHK-001', 'Basic Checking Account',     'Checking',    0.0100,   5.00),
    ('CHK-002', 'Premium Checking Account',   'Checking',    0.0150,  10.00),
    ('CRD-001', 'Standard Credit Card',       'Credit Card', 0.1999,   0.00),
    ('CRD-002', 'Premium Credit Card',        'Credit Card', 0.1499,   0.00),
    ('LN-001',  'Personal Loan',              'Loan',        0.0999, 100.00),
    ('LN-002',  'Home Loan',                  'Loan',        0.0499, 500.00),
    ('INV-001', 'Basic Investment Account',   'Investment',  0.0250,   0.00),
    ('INV-002', 'Premium Investment Account', 'Investment',  0.0300,   0.00)
) as v (code, name, category, rate, fee)
on conflict (product_code) do update set
    product_name     = excluded.product_name,
    product_category = excluded.product_category,
    interest_rate    = excluded.interest_rate,
    monthly_fee      = excluded.monthly_fee,
    updated_at       = now()
where (warehouse.dim_product.product_name,
       warehouse.dim_product.product_category,
       warehouse.dim_product.interest_rate,
       warehouse.dim_product.monthly_fee)
      is distinct from
      (excluded.product_name,
       excluded.product_category,
       excluded.interest_rate,
       excluded.monthly_fee);
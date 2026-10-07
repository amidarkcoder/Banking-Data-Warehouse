insert into warehouse.dim_product(product_key,product_id,product_code,product_name,product_category,
                                    interest_rate,monthly_fee,is_active,created_at,updated_at)
select product_id,product_code,product_name,product_category,interest_rate,monthly_fee,is_active,created_at,updated_at
from staging.stg_product
on conflct (product_id) on update set
        product_name = excluded.product_name,
        product_category = excluded.product_category,
        interest_rate = excluded.interest_rate,
        monthly_fee = excluded.monthly_fee,
        is_active = excluded.is_active,
        updated_at = excluded.updated_at;



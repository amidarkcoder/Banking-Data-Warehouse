select 'duplicate_customer_id' as check_name,'warehouse.dim_customer_scd3' as table_name, count(*) as failed_rows
from (select customer_id from warehouse.dim_customer_scd3 group by customer_id having count(*) > 1) x
union all
select 'duplicate_account_id','warehouse.dim_account', count(*) 
from (select account_id from warehouse.dim_account group by account_id having count(*) > 1) x
union all
select 'duplicate_product_id','warehouse.dim_product', count(*)
from (select product_id from warehouse.dim_product group by product_id having count(*) > 1) x
union all
select 'duplicate_branch_id','warehouse.dim_branch', count(*)
from (select branch_id from warehouse.dim_branch group by branch_id having count(*) > 1) x
union all
select 'duplicate_channel_id','warehouse.dim_channel', count(*)
from (select channel_id from warehouse.dim_channel group by channel_id having count(*) > 1) x
union all
select 'duplicate_transaction_id','warehouse.dim_transaction', count(*) 
from (select transaction_id from warehouse.dim_transaction group by transaction_id having count(*) > 1) x
union all
select 'duplicate_customer_id','staging.stg_customer', count(*) 
from (select customer_id from staging.stg_customer group by customer_id having count(*) > 1) x
union all
select 'duplicate_account_id','staging.stg_account', count(*) 
from (select account_id from staging.stg_account group by account_id having count(*) > 1) x
union all
select 'duplicate_transaction_id','staging.stg_transaction', count(*) 
from (select transaction_id from staging.stg_transaction group by transaction_id having count(*) > 1) x;



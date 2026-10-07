-- Pipeline health. Run the whole file in psql, or copy one query at a time.
-- Reads audit.pipeline_runs (filled by pipelines/common.py -> run_step).

-- 1. Latest run of each pipeline
SELECT DISTINCT ON (pipeline_name)
       pipeline_name, status, started_at, finished_at,
       round(extract(epoch FROM (finished_at - started_at))::numeric, 1) AS seconds,
       rows_written, error_message
FROM audit.pipeline_runs
ORDER BY pipeline_name, started_at DESC;

-- 2. Last 7 days per pipeline: how often it runs, fails and how long it takes
SELECT pipeline_name,
       count(*)                                    AS runs,
       count(*) FILTER (WHERE status = 'SUCCESS')  AS successes,
       count(*) FILTER (WHERE status = 'FAILED')   AS failures,
       round(avg(extract(epoch FROM (finished_at - started_at)))::numeric, 1) AS avg_seconds,
       coalesce(sum(rows_written), 0)              AS rows_written
FROM audit.pipeline_runs
WHERE started_at >= now() - interval '7 days'
GROUP BY pipeline_name
ORDER BY failures DESC, pipeline_name;

-- 3. Runs that look stuck (still RUNNING after 1 hour)
SELECT run_id, pipeline_name, started_at
FROM audit.pipeline_runs
WHERE status = 'RUNNING' AND started_at < now() - interval '1 hour'
ORDER BY started_at;

-- 4. Kafka backlog in raw.kafka_events
SELECT processing_status, count(*) AS events, min(ingested_at) AS oldest, max(ingested_at) AS newest
FROM raw.kafka_events
GROUP BY processing_status
ORDER BY processing_status;

-- 5. Row count of every table, layer by layer
SELECT 'raw'       AS layer, 'kafka_events'        AS table_name, count(*) AS row_count FROM raw.kafka_events
UNION ALL SELECT 'raw',       'customer_events',     count(*) FROM raw.customer_events
UNION ALL SELECT 'raw',       'account_events',      count(*) FROM raw.account_events
UNION ALL SELECT 'raw',       'transaction_events',  count(*) FROM raw.transaction_events
UNION ALL SELECT 'staging',   'stg_customer',        count(*) FROM staging.stg_customer
UNION ALL SELECT 'staging',   'stg_account',         count(*) FROM staging.stg_account
UNION ALL SELECT 'staging',   'stg_transaction',     count(*) FROM staging.stg_transaction
UNION ALL SELECT 'warehouse', 'dim_customer_scd3',   count(*) FROM warehouse.dim_customer_scd3
UNION ALL SELECT 'warehouse', 'dim_account',         count(*) FROM warehouse.dim_account
UNION ALL SELECT 'warehouse', 'dim_product',         count(*) FROM warehouse.dim_product
UNION ALL SELECT 'warehouse', 'dim_branch',          count(*) FROM warehouse.dim_branch
UNION ALL SELECT 'warehouse', 'dim_channel',         count(*) FROM warehouse.dim_channel
UNION ALL SELECT 'warehouse', 'dim_date',            count(*) FROM warehouse.dim_date
UNION ALL SELECT 'warehouse', 'fact_transactions',   count(*) FROM warehouse.fact_transactions;

-- 6. Data freshness: when did each layer last receive data?
SELECT 'raw.transaction_events (ingested_at)' AS source, max(ingested_at)::timestamp AS latest FROM raw.transaction_events
UNION ALL SELECT 'staging.stg_transaction (load_date)', max(load_date)::timestamp FROM staging.stg_transaction
UNION ALL SELECT 'warehouse.fact_transactions (loaded_at)', max(loaded_at) FROM warehouse.fact_transactions
UNION ALL SELECT 'warehouse.fact_transactions (newest transaction)', max(transaction_timestamp) FROM warehouse.fact_transactions;
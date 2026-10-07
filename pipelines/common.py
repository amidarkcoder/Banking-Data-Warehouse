"""Shared helpers: DB connection, SQL file runner, audit logging."""
import os
from pathlib import Path

import psycopg2

SQL_DIR = Path(__file__).resolve().parent.parent / "sql"


def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "enterprise_dw"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", ""),
    )


def run_step(pipeline_name, sql_files, params=None):
    """Run one or more SQL files (one statement each) and log to audit.pipeline_runs."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO audit.pipeline_runs (pipeline_name) VALUES (%s) RETURNING run_id",
                (pipeline_name,),
            )
            run_id = cur.fetchone()[0]
        conn.commit()

        try:
            total = 0
            with conn.cursor() as cur:
                for rel_path in sql_files:
                    cur.execute((SQL_DIR / rel_path).read_text(), params)
                    written = max(cur.rowcount, 0)
                    print(f"[{pipeline_name}] {rel_path}: {written} rows")
                    total += written
                cur.execute(
                    "UPDATE audit.pipeline_runs SET status='SUCCESS', finished_at=now(), "
                    "rows_written=%s WHERE run_id=%s",
                    (total, run_id),
                )
            conn.commit()
        except Exception as exc:
            conn.rollback()
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE audit.pipeline_runs SET status='FAILED', finished_at=now(), "
                    "error_message=%s WHERE run_id=%s",
                    (str(exc), run_id),
                )
            conn.commit()
            raise
    finally:
        conn.close()

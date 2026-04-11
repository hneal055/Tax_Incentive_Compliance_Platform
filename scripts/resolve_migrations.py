#!/usr/bin/env python3
"""
resolve_migrations.py
=====================
Marks known-failed Prisma migrations as finished in the _prisma_migrations
table so that `prisma migrate deploy` can proceed without hitting P3009.

Migrations resolved:
  - 20260410000001_add_sub_jurisdiction_layer
  - 20260411000002_phase0_stacking_engine

Only rows where finished_at IS NULL are updated, making this script safe to
run multiple times (idempotent).

Usage:
    python scripts/resolve_migrations.py

Requires:
    DATABASE_URL environment variable pointing to the target PostgreSQL database.
    psycopg2-binary (already listed in requirements.txt).
"""

import os
import sys

import psycopg2

FAILED_MIGRATIONS = [
    "20260410000001_add_sub_jurisdiction_layer",
    "20260411000002_phase0_stacking_engine",
]

UPDATE_SQL = """
UPDATE _prisma_migrations
SET    finished_at = NOW(),
       logs        = 'Manually resolved'
WHERE  migration_name = %s
  AND  finished_at IS NULL;
"""


def main() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("[ERROR] DATABASE_URL environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    print("[INFO]  Connecting to database...")
    try:
        conn = psycopg2.connect(database_url)
    except psycopg2.OperationalError as exc:
        print(f"[ERROR] Could not connect to the database: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        with conn:
            with conn.cursor() as cur:
                for migration_name in FAILED_MIGRATIONS:
                    cur.execute(UPDATE_SQL, (migration_name,))
                    rows_affected = cur.rowcount
                    if rows_affected > 0:
                        print(
                            f"[OK]    Marked as finished: {migration_name} "
                            f"({rows_affected} row updated)"
                        )
                    else:
                        print(
                            f"[INFO]  Already finished or not found, skipping: "
                            f"{migration_name}"
                        )
    except psycopg2.Error as exc:
        print(f"[ERROR] Database error while updating migrations: {exc}", file=sys.stderr)
        sys.exit(1)
    finally:
        conn.close()

    print("[INFO]  Migration resolution complete.")


if __name__ == "__main__":
    main()

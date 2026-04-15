"""
seed_maximizer_test.py
======================
Inserts sample local_rules for NY, CA, and IL so the Maximizer
returns non-zero values when tested.

Run from project root:
    python scripts/seed_maximizer_test.py

Requires DATABASE_URL in environment (or .env file).
Safe to re-run — uses INSERT ... ON CONFLICT DO NOTHING.
"""

import os
import sys
from datetime import datetime

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

RULES = [
    # (jurisdiction_code, name, code, category, ruleType, amount, percentage, description, sourceUrl)
    (
        "NY",
        "New York State Film Tax Credit",
        "NY-FILM-TAX-CREDIT",
        "film_incentive",
        "tax_credit",
        None,
        30.0,
        "30% refundable tax credit on qualified production expenses in New York State.",
        "https://www.nyc.gov/site/mome/incentives/tax-credit.page",
    ),
    (
        "NY",
        "New York City Additional Credit",
        "NYC-ADDITIONAL-CREDIT",
        "local_incentive",
        "tax_credit",
        None,
        10.0,
        "Additional 10% credit for productions shooting in NYC qualifying locations.",
        "https://www.nyc.gov/site/mome/incentives/tax-credit.page",
    ),
    (
        "CA",
        "California Film & TV Tax Credit",
        "CA-FILM-TAX-CREDIT",
        "film_incentive",
        "tax_credit",
        None,
        25.0,
        "25% transferable tax credit on qualified expenditures for productions filming in California.",
        "https://film.ca.gov/tax-credit/",
    ),
    (
        "CA",
        "California Soundstage Filming Credit",
        "CA-SOUNDSTAGE-BONUS",
        "film_incentive",
        "rebate",
        None,
        5.0,
        "Additional 5% credit for productions using certified California soundstages.",
        "https://film.ca.gov/tax-credit/",
    ),
    (
        "IL",
        "Illinois Film Production Credit",
        "IL-FILM-BASE",
        "film_incentive",
        "tax_credit",
        None,
        30.0,
        "30% tax credit on Illinois production spending for qualified film and TV productions.",
        "https://www.illinois.gov/content/dam/soi/en/web/dceo/docs/film-production-services-act.pdf",
    ),
    (
        "IL",
        "Chicago Location Bonus",
        "IL-CHICAGO-BONUS",
        "local_incentive",
        "rebate",
        None,
        15.0,
        "Additional 15% rebate for qualifying Chicago-based productions.",
        "https://www.chicago.gov/city/en/depts/dca/supp_info/chicago_film_office.html",
    ),
    (
        "GA",
        "Georgia Entertainment Industry Investment Act",
        "GA-FILM-CREDIT",
        "film_incentive",
        "tax_credit",
        None,
        20.0,
        "20% tax credit on all Georgia qualified production expenditures.",
        "https://www.georgia.org/film-music-digital-entertainment/georgia-film-tv-production",
    ),
    (
        "GA",
        "Georgia Qualified Logo Bonus",
        "GA-LOGO-BONUS",
        "film_incentive",
        "tax_credit",
        None,
        10.0,
        "Additional 10% credit for including the Georgia promotional logo in the production.",
        "https://www.georgia.org/film-music-digital-entertainment/georgia-film-tv-production",
    ),
]


def main() -> None:
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("[ERROR] DATABASE_URL not set.", file=sys.stderr)
        sys.exit(1)

    conn = psycopg2.connect(database_url)

    with conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Build code → id map for the jurisdictions we need
            codes = list({r[0] for r in RULES})
            cur.execute(
                "SELECT id, code FROM jurisdictions WHERE code = ANY(%s)",
                (codes,),
            )
            jmap = {row["code"]: row["id"] for row in cur.fetchall()}

            missing = [c for c in codes if c not in jmap]
            if missing:
                print(f"[WARN] Jurisdictions not found in DB (skipping): {missing}")

            inserted = 0
            skipped = 0
            for jcode, name, code, category, rule_type, amount, percentage, description, source_url in RULES:
                jid = jmap.get(jcode)
                if not jid:
                    continue

                cur.execute(
                    """
                    INSERT INTO local_rules (
                        id, "jurisdictionId", name, code, category, "ruleType",
                        amount, percentage, description, "effectiveDate",
                        "sourceUrl", "extractedBy", active,
                        "createdAt", "updatedAt"
                    ) VALUES (
                        gen_random_uuid(), %s, %s, %s, %s, %s,
                        %s, %s, %s, %s,
                        %s, 'manual', true,
                        NOW(), NOW()
                    )
                    ON CONFLICT (code) DO NOTHING
                    """,
                    (
                        jid, name, code, category, rule_type,
                        amount, percentage, description,
                        datetime(2024, 1, 1),
                        source_url,
                    ),
                )
                if cur.rowcount:
                    inserted += 1
                    print(f"[OK]    Inserted: {code}")
                else:
                    skipped += 1
                    print(f"[INFO]  Already exists, skipped: {code}")

    conn.close()
    print(f"\n[DONE] {inserted} inserted, {skipped} skipped.")


if __name__ == "__main__":
    main()

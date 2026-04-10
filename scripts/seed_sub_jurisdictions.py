"""
Seed initial sub-jurisdictions for testing.
Creates Erie, Nassau, and Westchester counties linked to New York state.

Run inside the container:
    docker exec pilotforge-api python scripts/seed_sub_jurisdictions.py

Or locally with DATABASE_URL set:
    python scripts/seed_sub_jurisdictions.py
"""

import asyncio
import os
import sys
import logging
from datetime import datetime, timezone

from dotenv import load_dotenv
load_dotenv()

from prisma import Prisma

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

# Sub-jurisdictions to seed
# feedUrl points to an official government page to monitor for changes.
COUNTIES = [
    {
        "name": "Erie County",
        "code": "NY-ERIE",
        "parentCode": "NY",
        "country": "US",
        "type": "county",
        "description": "Erie County, New York — home to Buffalo. County-level filming permits and fees.",
        "website": "https://www2.erie.gov",
        "feedUrl": "https://www2.erie.gov/legislature/",
        "currency": "USD",
    },
    {
        "name": "Nassau County",
        "code": "NY-NASSAU",
        "parentCode": "NY",
        "country": "US",
        "type": "county",
        "description": "Nassau County, New York — Long Island. County permit and fee schedules.",
        "website": "https://www.nassaucountyny.gov",
        "feedUrl": "https://www.nassaucountyny.gov/",
        "currency": "USD",
    },
    {
        "name": "Westchester County",
        "code": "NY-WESTCHESTER",
        "parentCode": "NY",
        "country": "US",
        "type": "county",
        "description": "Westchester County, New York. Active film office with permit requirements.",
        "website": "https://www.westchestergov.com",
        "feedUrl": "https://www.westchestergov.com/planning",
        "currency": "USD",
    },
]

# Default inheritance policy: counties inherit state incentives additively
# (county rules add on top of state rules rather than replacing them)
INHERITANCE_POLICY = {
    "policyType": "additive",
    "ruleCategory": None,   # applies to all categories
    "priority": 10,
    "notes": "County rules are applied in addition to New York state incentives.",
}


async def main():
    db = Prisma()
    await db.connect()

    try:
        # ── Find New York state jurisdiction ──────────────────────────────────
        ny = await db.jurisdiction.find_unique(where={"code": "NY"})
        if not ny:
            log.error("New York (code='NY') not found in jurisdictions table.")
            log.error("Run seed_jurisdictions.py first, then re-run this script.")
            sys.exit(1)

        log.info(f"Found parent jurisdiction: {ny.name} (id={ny.id})")

        seeded = 0
        for county in COUNTIES:
            existing = await db.jurisdiction.find_unique(where={"code": county["code"]})

            if existing:
                log.info(f"  {county['code']} already exists — skipping")
                jur_id = existing.id
            else:
                now = datetime.now(timezone.utc)
                new_jur = await db.jurisdiction.create(
                    data={
                        "name":        county["name"],
                        "code":        county["code"],
                        "country":     county["country"],
                        "type":        county["type"],
                        "description": county["description"],
                        "website":     county["website"],
                        "feedUrl":     county["feedUrl"],
                        "currency":    county["currency"],
                        "parentId":    ny.id,
                        "active":      True,
                        "updatedAt":   now,
                    }
                )
                jur_id = new_jur.id
                log.info(f"  Created {county['code']} — {county['name']}")
                seeded += 1

            # ── Inheritance policy (idempotent) ───────────────────────────────
            try:
                await db.inheritancepolicy.create(
                    data={
                        "childJurisdictionId":  jur_id,
                        "parentJurisdictionId": ny.id,
                        "policyType":           INHERITANCE_POLICY["policyType"],
                        "ruleCategory":         INHERITANCE_POLICY["ruleCategory"],
                        "priority":             INHERITANCE_POLICY["priority"],
                        "notes":                INHERITANCE_POLICY["notes"],
                        "updatedAt":            datetime.now(timezone.utc),
                    }
                )
                log.info(f"    Inheritance policy set: {county['code']} → NY (additive)")
            except Exception:
                log.info(f"    Inheritance policy already exists for {county['code']} — skipping")

        log.info("")
        log.info(f"Done — {seeded} new county jurisdiction(s) created.")
        log.info("Run monitor.py to test feed fetching and Claude extraction.")

    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

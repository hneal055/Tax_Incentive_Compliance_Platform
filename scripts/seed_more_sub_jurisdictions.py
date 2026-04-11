"""
Seed LA County, Cook County (Chicago), and NYC boroughs as sub-jurisdictions.

Run inside the container:
    docker exec pilotforge-api python scripts/seed_more_sub_jurisdictions.py

Or locally with DATABASE_URL set:
    python scripts/seed_more_sub_jurisdictions.py
"""

import asyncio
import logging
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
load_dotenv()

from prisma import Prisma

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)


# ── Sub-jurisdictions to seed ────────────────────────────────────────────────

SUB_JURISDICTIONS = [
    # ── Los Angeles County (CA) ───────────────────────────────────────────────
    {
        "name": "Los Angeles County",
        "code": "CA-LA",
        "parentCode": "CA",
        "country": "US",
        "type": "county",
        "description": (
            "Los Angeles County, California — the world's largest film production center. "
            "FilmLA administers permits and incentive programs."
        ),
        "website": "https://www.filmla.com",
        "feedUrl": "https://www.filmla.com/for-filmmakers/permits/",
        "currency": "USD",
        "inheritanceNotes": "LA County rules add on top of California state incentives.",
    },

    # ── Cook County / Chicago (IL) ────────────────────────────────────────────
    {
        "name": "Cook County",
        "code": "IL-COOK",
        "parentCode": "IL",
        "country": "US",
        "type": "county",
        "description": (
            "Cook County, Illinois — includes City of Chicago. "
            "Chicago Film Office coordinates production permits and the Chicago location bonus."
        ),
        "website": "https://www.chicago.gov/city/en/depts/dca/supp_info/chicago_film_office.html",
        "feedUrl": "https://www.chicago.gov/city/en/depts/dca/supp_info/chicago_film_office.html",
        "currency": "USD",
        "inheritanceNotes": "Cook County rules add on top of Illinois state incentives.",
    },

    # ── NYC Boroughs (NY) ─────────────────────────────────────────────────────
    {
        "name": "New York City",
        "code": "NY-NYC",
        "parentCode": "NY",
        "country": "US",
        "type": "city",
        "description": (
            "New York City — all five boroughs. Mayor's Office of Media and Entertainment "
            "administers film permits and the NYC 5% location incentive bonus."
        ),
        "website": "https://www.nyc.gov/mome",
        "feedUrl": "https://www.nyc.gov/site/mome/industries/film-tv-production.page",
        "currency": "USD",
        "inheritanceNotes": "NYC rules add on top of New York state incentives.",
    },
    {
        "name": "Brooklyn",
        "code": "NY-BROOKLYN",
        "parentCode": "NY",
        "country": "US",
        "type": "county",
        "description": (
            "Brooklyn (Kings County), New York City. "
            "Popular production location; covered under NYC Mayor's Office permits."
        ),
        "website": "https://www.nyc.gov/mome",
        "feedUrl": "https://www.nyc.gov/site/mome/industries/film-tv-production.page",
        "currency": "USD",
        "inheritanceNotes": "Brooklyn rules add on top of New York state incentives.",
    },
    {
        "name": "Queens",
        "code": "NY-QUEENS",
        "parentCode": "NY",
        "country": "US",
        "type": "county",
        "description": (
            "Queens County, New York City — home to Kaufman Astoria Studios and Silvercup. "
            "Covered under NYC Mayor's Office permits."
        ),
        "website": "https://www.nyc.gov/mome",
        "feedUrl": "https://www.nyc.gov/site/mome/industries/film-tv-production.page",
        "currency": "USD",
        "inheritanceNotes": "Queens rules add on top of New York state incentives.",
    },
    {
        "name": "Manhattan",
        "code": "NY-MANHATTAN",
        "parentCode": "NY",
        "country": "US",
        "type": "county",
        "description": (
            "Manhattan (New York County) — highest-demand filming location. "
            "Covered under NYC Mayor's Office permits."
        ),
        "website": "https://www.nyc.gov/mome",
        "feedUrl": "https://www.nyc.gov/site/mome/industries/film-tv-production.page",
        "currency": "USD",
        "inheritanceNotes": "Manhattan rules add on top of New York state incentives.",
    },
    {
        "name": "Bronx",
        "code": "NY-BRONX",
        "parentCode": "NY",
        "country": "US",
        "type": "county",
        "description": (
            "Bronx County, New York City. Emerging production location. "
            "Covered under NYC Mayor's Office permits."
        ),
        "website": "https://www.nyc.gov/mome",
        "feedUrl": "https://www.nyc.gov/site/mome/industries/film-tv-production.page",
        "currency": "USD",
        "inheritanceNotes": "Bronx rules add on top of New York state incentives.",
    },
    {
        "name": "Staten Island",
        "code": "NY-STATEN-ISLAND",
        "parentCode": "NY",
        "country": "US",
        "type": "county",
        "description": (
            "Staten Island (Richmond County), New York City. "
            "Covered under NYC Mayor's Office permits."
        ),
        "website": "https://www.nyc.gov/mome",
        "feedUrl": "https://www.nyc.gov/site/mome/industries/film-tv-production.page",
        "currency": "USD",
        "inheritanceNotes": "Staten Island rules add on top of New York state incentives.",
    },
]


async def main():
    db = Prisma()
    await db.connect()

    try:
        # ── Load parent jurisdictions ─────────────────────────────────────────
        parents: dict[str, object] = {}
        for code in ("CA", "IL", "NY"):
            jur = await db.jurisdiction.find_unique(where={"code": code})
            if not jur:
                log.error(f"Parent jurisdiction '{code}' not found. Run seed_jurisdictions.py first.")
                sys.exit(1)
            parents[code] = jur
            log.info(f"Found parent: {jur.name} ({jur.code})")

        seeded = 0
        for item in SUB_JURISDICTIONS:
            parent = parents[item["parentCode"]]
            existing = await db.jurisdiction.find_unique(where={"code": item["code"]})

            if existing:
                log.info(f"  {item['code']} already exists — skipping")
                jur_id = existing.id
            else:
                now = datetime.now(timezone.utc)
                new_jur = await db.jurisdiction.create(
                    data={
                        "name":        item["name"],
                        "code":        item["code"],
                        "country":     item["country"],
                        "type":        item["type"],
                        "description": item["description"],
                        "website":     item["website"],
                        "feedUrl":     item["feedUrl"],
                        "currency":    item["currency"],
                        "parentId":    parent.id,
                        "active":      True,
                        "updatedAt":   now,
                    }
                )
                jur_id = new_jur.id
                log.info(f"  Created {item['code']} — {item['name']}")
                seeded += 1

            # ── Inheritance policy (idempotent) ───────────────────────────────
            try:
                await db.inheritancepolicy.create(
                    data={
                        "childJurisdictionId":  jur_id,
                        "parentJurisdictionId": parent.id,
                        "policyType":           "additive",
                        "ruleCategory":         None,
                        "priority":             10,
                        "notes":                item["inheritanceNotes"],
                        "updatedAt":            datetime.now(timezone.utc),
                    }
                )
                log.info(f"    Inheritance policy: {item['code']} → {item['parentCode']} (additive)")
            except Exception:
                log.info(f"    Inheritance policy already exists for {item['code']} — skipping")

        log.info("")
        log.info(f"Done — {seeded} new sub-jurisdiction(s) created.")
        log.info("Run monitor.py to trigger feed checks for the new sub-jurisdictions.")

    finally:
        await db.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

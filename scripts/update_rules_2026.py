"""
2026 incentive rule updates — applies to the live database.

Changes:
  UK-FILM-BASE  : renamed to AVEC, rate 25% → 34%  (effective 1 Jan 2024)
  UK-AVEC-ANIMATION: new rule at 39% for animation & children's TV

Run inside the container:
  docker exec pilotforge-api python scripts/update_rules_2026.py
"""
import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.database import prisma


async def main():
    await prisma.connect()
    print("Connected to database\n")

    # ── 1. Update UK-FILM-BASE: old Film Tax Relief → AVEC ────────────────────
    uk_base = await prisma.incentiverule.find_first(where={"ruleCode": "UK-FILM-BASE"})
    if uk_base:
        old_pct = uk_base.percentage
        await prisma.incentiverule.update(
            where={"id": uk_base.id},
            data={
                "ruleName": "UK Audio-Visual Expenditure Credit (AVEC) — Film & HETV",
                "percentage": 34.0,
                "minSpend": None,
                "requirements": json.dumps({
                    "ukSpend": 10,
                    "culturalTest": True,
                    "ukProduction": True,
                    "hETV_minBudgetPerEpisode": 1_000_000,
                }),
            },
        )
        print(f"✅ UK-FILM-BASE updated: {old_pct}% → 34%  (AVEC)")
    else:
        print("⚠️  UK-FILM-BASE not found — skipping")

    # ── 2. Add UK-AVEC-ANIMATION if not present ───────────────────────────────
    existing_anim = await prisma.incentiverule.find_first(
        where={"ruleCode": "UK-AVEC-ANIMATION"}
    )
    if existing_anim:
        print("⏭️  UK-AVEC-ANIMATION already exists — skipping")
    else:
        uk_jur = await prisma.jurisdiction.find_first(where={"code": "UK"})
        if uk_jur:
            await prisma.incentiverule.create(
                data={
                    "ruleCode": "UK-AVEC-ANIMATION",
                    "ruleName": "UK Audio-Visual Expenditure Credit (AVEC) — Animation & Children's TV",
                    "incentiveType": "tax_credit",
                    "percentage": 39.0,
                    "eligibleExpenses": ["uk_core_expenditure"],
                    "excludedExpenses": ["marketing", "distribution"],
                    "effectiveDate": datetime(2024, 1, 1),
                    "requirements": json.dumps({
                        "ukSpend": 10,
                        "culturalTest": True,
                        "animationOrChildrensTV": True,
                    }),
                    "active": True,
                    "jurisdiction": {"connect": {"id": uk_jur.id}},
                }
            )
            print("✅ UK-AVEC-ANIMATION created at 39%")
        else:
            print("⚠️  UK jurisdiction not found — cannot create animation rule")

    await prisma.disconnect()
    print("\nDone — 2026 rule updates applied.")


if __name__ == "__main__":
    asyncio.run(main())

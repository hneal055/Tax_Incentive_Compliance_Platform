"""
seed_ny_fix.py — Add Made in NY program rules to Brooklyn, Queens, NY-NYC
==========================================================================
Bronx, Manhattan, and Staten Island already have 6 NYC program rules each.
Brooklyn, Queens, and the catch-all NY-NYC entity are missing them.
Nassau, Westchester, and Erie are outside NYC — correctly have no NYC programs.
"""
import os, sys, uuid
from datetime import datetime, timezone
import psycopg2

DB_URL = os.environ.get("DATABASE_URL")
if not DB_URL:
    sys.exit("DATABASE_URL not set")

conn = psycopg2.connect(DB_URL)
conn.autocommit = False
cur = conn.cursor()
NOW = datetime.now(timezone.utc)
EFF = datetime(2024, 1, 1, tzinfo=timezone.utc)

# NYC program rule templates — replicated for each missing borough
NYC_PROGRAMS = [
    {
        'suffix':        'CITY-OWNED-LOCATION-FEES',
        'name':          'City-Owned Location Fees',
        'incentiveType': 'permit_fee',
        'creditType':    'non_refundable',
        'percentage':    None,
        'requirements':  'Applicable to productions seeking to film at City-owned locations. Fee applicability depends on whether the location is managed by DCAS.',
    },
    {
        'suffix':        'MADE-IN-NY-DISCOUNT-CARD',
        'name':          'Made in NY Discount Card',
        'incentiveType': 'exemption',
        'creditType':    'non_refundable',
        'percentage':    None,
        'requirements':  'Must be a bona fide production filming in New York City to qualify for the card.',
    },
    {
        'suffix':        'MADE-IN-NY-MARKETING-CREDIT',
        'name':          'Made in NY Marketing Credit',
        'incentiveType': 'tax_credit',
        'creditType':    'non_refundable',
        'percentage':    None,
        'requirements':  'At least 75% of the film must have been produced in New York City. Program is currently on hold.',
    },
    {
        'suffix':        'MADE-IN-NY-PA-TRAINING-PROGRAM',
        'name':          'Made in NY PA Training Program - Free Placement Service',
        'incentiveType': 'requirement',
        'creditType':    'non_refundable',
        'percentage':    None,
        'requirements':  'Production must be shooting in NYC or surrounding areas. Service is free of charge.',
    },
    {
        'suffix':        'MATERIALS-FOR-THE-ARTS',
        'name':          'Materials for the Arts - Production Strike/Liquidation',
        'incentiveType': 'requirement',
        'creditType':    'non_refundable',
        'percentage':    None,
        'requirements':  'Available to productions operating in New York City seeking strike or liquidation support.',
    },
    {
        'suffix':        'NYC-FILM-GREEN-SUSTAINABILITY',
        'name':          'NYC Film Green Sustainability Program',
        'incentiveType': 'requirement',
        'creditType':    'non_refundable',
        'percentage':    None,
        'requirements':  'Voluntary participation. Productions must engage in environmentally-conscious practices to apply for recognition.',
    },
]

# Boroughs to fix
TARGETS = ['NY-BROOKLYN', 'NY-QUEENS', 'NY-NYC']

for borough_code in TARGETS:
    cur.execute("SELECT id FROM jurisdictions WHERE code = %s", (borough_code,))
    row = cur.fetchone()
    if not row:
        print(f"[SKIP] {borough_code} not found in DB")
        continue
    jur_id = row[0]

    for prog in NYC_PROGRAMS:
        rule_code = f"{borough_code}-{prog['suffix']}"
        cur.execute('SELECT id FROM incentive_rules WHERE "ruleCode" = %s', (rule_code,))
        if cur.fetchone():
            print(f"[--] {rule_code} already exists")
            continue
        cur.execute("""
            INSERT INTO incentive_rules (
                id, "jurisdictionId", "ruleName", "ruleCode",
                "incentiveType", "creditType", percentage,
                "eligibleExpenses", "excludedExpenses",
                "effectiveDate", requirements,
                active, "createdAt", "updatedAt"
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,true,%s,%s)
        """, (
            str(uuid.uuid4()), jur_id,
            prog['name'], rule_code,
            prog['incentiveType'], prog['creditType'], prog['percentage'],
            '{}', '{}',
            EFF, prog['requirements'],
            NOW, NOW
        ))
        print(f"[ok] {rule_code} inserted")

conn.commit()
conn.close()
print("\nDone. NYC program rules applied to Brooklyn, Queens, NY-NYC.")

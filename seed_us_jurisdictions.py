"""
Seed US state jurisdictions and film/TV incentive rules via the REST API.
Run with: python seed_us_jurisdictions.py
Requires the API server running on http://127.0.0.1:8080
"""
import requests
import sys

BASE = "https://pilotforge-5wiz.onrender.com/api/v1"

# ---------- US states with active film/TV incentive programs ----------
# Source: state film commission public data (rates as of 2025-2026)
STATES = [
    # (code, name, description, website)
    ("AL", "Alabama", "Alabama Film Incentive - 25% rebate on qualifying spend", "https://www.alabamafilm.org"),
    ("AK", "Alaska", "Alaska Film Production Tax Credit - 30-36% transferable credit", "https://prior.prior.prior"),
    ("AR", "Arkansas", "Arkansas Film Incentive - 20% rebate on qualifying spend", "https://www.arkansasedc.com/film"),
    ("CO", "Colorado", "Colorado Film Incentive - 20% cash rebate on qualifying spend", "https://oedit.colorado.gov/colorado-office-of-film-television-media"),
    ("CT", "Connecticut", "Connecticut Film Production Tax Credit - 10-30% credit", "https://ctfilm.com"),
    ("FL", "Florida", "Florida Film & Entertainment Industry Financial Incentive Program", "https://filminflorida.com"),
    ("HI", "Hawaii", "Hawaii Motion Picture, Digital Media & Film Production Tax Credit - 20-25%", "https://filmoffice.hawaii.gov"),
    ("ID", "Idaho", "Idaho Film Rebate Program - 20% on qualifying spend", "https://commerce.idaho.gov/industries/film"),
    ("IN", "Indiana", "Indiana Economic Development for a Growing Economy (EDGE) Credit", "https://iedc.in.gov"),
    ("KY", "Kentucky", "Kentucky Film Industry Tax Credit - 30-35% on qualifying spend", "https://filmoffice.ky.gov"),
    ("ME", "Maine", "Maine Attraction Film Incentive - 5% wage rebate + 10% non-resident", "https://www.filminmaine.com"),
    ("MD", "Maryland", "Maryland Film Production Activity Tax Credit - 25-27% credit", "https://commerce.maryland.gov/fund/maryland-film-production-employment-act"),
    ("MA", "Massachusetts", "Massachusetts Film Tax Incentive - 25% credit", "https://www.mafilm.org"),
    ("MN", "Minnesota", "Minnesota Snowbate Film Incentive - 25% rebate on qualifying spend", "https://mnfilmtv.org"),
    ("MS", "Mississippi", "Mississippi Motion Picture Incentive - 25-30% rebate", "https://www.filmmississippi.org"),
    ("MO", "Missouri", "Missouri Film Production Tax Credit - 20% on qualifying spend", "https://mofilm.org"),
    ("MT", "Montana", "Montana Big Sky Film Grant - 20% on qualifying spend", "https://www.montanafilm.com"),
    ("NV", "Nevada", "Nevada Film Tax Credit - 15-25% transferable credit", "https://nevadafilm.com"),
    ("NJ", "New Jersey", "New Jersey Film & Digital Media Tax Credit - 30-37% credit", "https://www.njeda.gov/film"),
    ("NC", "North Carolina", "North Carolina Film & Entertainment Grant - 25% grant", "https://filmnc.com"),
    ("OH", "Ohio", "Ohio Motion Picture Tax Credit - 30% on qualifying spend", "https://development.ohio.gov/business/state-incentives/ohio-motion-picture-tax-credit"),
    ("OK", "Oklahoma", "Oklahoma Film Enhancement Rebate - 20-37% rebate", "https://okfilmmusic.org"),
    ("OR", "Oregon", "Oregon Production Investment Fund (OPIF) - 20-26.2% rebate", "https://oregonfilm.org"),
    ("PA", "Pennsylvania", "Pennsylvania Film Production Tax Credit - 25-30% credit", "https://filminpa.com"),
    ("RI", "Rhode Island", "Rhode Island Motion Picture Production Tax Credit - 25-30%", "https://www.arts.ri.gov/initiatives/film"),
    ("SC", "South Carolina", "South Carolina Film Incentive - 25-30% on qualifying spend", "https://www.filmsc.com"),
    ("TN", "Tennessee", "Tennessee Film, TV & Music Fund - 25% grant", "https://www.tn.gov/transparenttn/open-ecd/openecd/tnecd-programs-activities/redirect-film--entertainment---music-incentive-program/film--entertainment---music-incentive-program.html"),
    ("UT", "Utah", "Utah Motion Picture Incentive - 20-25% tax credit or cash rebate", "https://film.utah.gov"),
    ("VA", "Virginia", "Virginia Motion Picture Tax Credit - 15-20% credit", "https://www.virginia.org/film"),
    ("WA", "Washington", "Washington Motion Picture Competitiveness Program - B&O tax credit", "https://washingtonfilmworks.org"),
    ("WV", "West Virginia", "West Virginia Film Industry Investment Act - 27-31% credit", "https://wvfilm.com"),
    ("WI", "Wisconsin", "Wisconsin Film Production Services Credit - 25% on qualifying spend", "https://wedc.org"),
    ("WY", "Wyoming", "Wyoming Film Industry Financial Incentive - 15% cash rebate", "https://wyofilm.org"),
    ("DC", "District of Columbia", "DC Film Incentive - up to 35% rebate on qualifying expenditures", "https://entertainment.dc.gov"),
]

# Rules for each state (code, ruleName, ruleCode, incentiveType, percentage, minSpend, maxCredit, eligible, excluded, requirements)
RULES = [
    ("AL", "Alabama Film Incentive Rebate", "AL-FIR-2025", "rebate", 25.0, 500000, 0, ["production_costs", "crew_wages", "equipment"], ["marketing", "distribution"], {"base_rebate": "25% rebate on qualifying Alabama spend", "minimum_spend": "$500K", "additional_bonus": "Additional 5% for episodic TV"}),
    ("AK", "Alaska Film Production Tax Credit", "AK-FPTC-2025", "tax_credit", 30.0, 75000, 0, ["production_costs", "labor", "equipment"], ["marketing"], {"base_credit": "30% transferable tax credit", "rural_bonus": "Additional 6% for rural areas (total 36%)", "min_spend": "$75,000"}),
    ("AR", "Arkansas Film Incentive Rebate", "AR-FIR-2025", "rebate", 20.0, 200000, 0, ["production_costs", "labor"], ["marketing", "distribution"], {"base_rebate": "20% rebate", "minimum_spend": "$200K in-state"}),
    ("CO", "Colorado Film Incentive Cash Rebate", "CO-FICR-2025", "rebate", 20.0, 100000, 0, ["production_costs", "labor", "equipment"], ["marketing"], {"base_rebate": "20% cash rebate", "minimum_spend": "$100K"}),
    ("CT", "Connecticut Film Production Tax Credit", "CT-FPTC-2025", "tax_credit", 10.0, 100000, 0, ["production_costs", "labor", "equipment"], ["marketing", "distribution"], {"base_credit": "10-30% credit depending on spend", "infrastructure_bonus": "Up to 30% for infrastructure projects"}),
    ("FL", "Florida Entertainment Industry Incentive", "FL-EIIP-2025", "grant", 15.0, 625000, 0, ["production_costs", "labor"], ["marketing"], {"base_grant": "15% on qualifying spend", "family_friendly_bonus": "Additional 5% for family-friendly content", "min_spend": "$625K"}),
    ("HI", "Hawaii Motion Picture Tax Credit", "HI-MPTC-2025", "tax_credit", 20.0, 200000, 0, ["production_costs", "labor", "post_production"], ["marketing", "distribution"], {"base_credit": "20% on Oahu, 25% on neighbor islands", "minimum_spend": "$200K"}),
    ("ID", "Idaho Film Rebate", "ID-FR-2025", "rebate", 20.0, 200000, 0, ["production_costs", "labor"], ["marketing"], {"base_rebate": "20% rebate", "minimum_spend": "$200K in-state"}),
    ("IN", "Indiana EDGE Film Credit", "IN-EDGE-2025", "tax_credit", 15.0, 50000, 0, ["production_costs", "labor"], ["marketing"], {"credit": "Up to 15% on qualifying spend", "min_spend": "$50K"}),
    ("KY", "Kentucky Film Industry Tax Credit", "KY-FITC-2025", "tax_credit", 30.0, 250000, 0, ["production_costs", "labor", "equipment", "post_production"], ["marketing", "distribution"], {"base_credit": "30% on labor, 35% on non-resident labor", "minimum_spend": "$250K"}),
    ("ME", "Maine Attraction Film Incentive", "ME-AFI-2025", "rebate", 12.0, 75000, 0, ["wages", "production_costs"], ["marketing"], {"wage_rebate": "5% on wages for residents, 10-12% for non-residents", "visual_media_fund": "Uncapped incentive"}),
    ("MD", "Maryland Film Production Activity Tax Credit", "MD-FPATC-2025", "tax_credit", 25.0, 250000, 0, ["production_costs", "labor", "equipment"], ["marketing", "distribution"], {"base_credit": "25% on total direct costs", "television_bonus": "Additional 2% for TV series (27%)", "minimum_spend": "$250K"}),
    ("MA", "Massachusetts Film Tax Incentive", "MA-FTI-2025", "tax_credit", 25.0, 50000, 0, ["production_costs", "payroll"], ["marketing", "distribution"], {"payroll_credit": "25% credit on payroll", "production_credit": "25% on production spend over $50K", "sales_tax_exemption": "Sales tax exemption included"}),
    ("MN", "Minnesota Snowbate Film Incentive", "MN-SFI-2025", "rebate", 25.0, 0, 0, ["production_costs", "labor"], ["marketing"], {"base_rebate": "25% rebate on qualifying spend", "no_minimum": "No minimum spend requirement"}),
    ("MS", "Mississippi Motion Picture Incentive", "MS-MPI-2025", "rebate", 25.0, 50000, 0, ["production_costs", "labor", "equipment"], ["marketing", "distribution"], {"base_rebate": "25% rebate on qualifying spend", "payroll_bonus": "Additional 5% on resident payroll (total 30%)", "minimum_spend": "$50K"}),
    ("MO", "Missouri Film Production Tax Credit", "MO-FPTC-2025", "tax_credit", 20.0, 50000, 0, ["production_costs", "labor"], ["marketing", "distribution"], {"base_credit": "20% on qualifying expenses", "minimum_spend": "$50K"}),
    ("MT", "Montana Big Sky Film Grant", "MT-BSFG-2025", "grant", 20.0, 50000, 0, ["production_costs", "labor"], ["marketing"], {"base_grant": "20% cash rebate", "minimum_spend": "$50K qualifying Montana expenditures"}),
    ("NV", "Nevada Film Tax Credit", "NV-FTC-2025", "tax_credit", 15.0, 500000, 6000000, ["production_costs", "labor", "equipment"], ["marketing"], {"base_credit": "15% transferable credit", "additional_credits": "Additional 5-10% for various bonuses (up to 25%)", "minimum_spend": "$500K", "annual_cap": "$6M per production"}),
    ("NJ", "New Jersey Film & Digital Media Tax Credit", "NJ-FDMTC-2025", "tax_credit", 30.0, 1000000, 0, ["production_costs", "labor", "post_production"], ["marketing", "distribution"], {"base_credit": "30% on qualifying expenses", "diversity_bonus": "Additional 2-7% for diversity criteria (up to 37%)", "minimum_spend": "$1M"}),
    ("NC", "North Carolina Film & Entertainment Grant", "NC-FEG-2025", "grant", 25.0, 250000, 12000000, ["production_costs", "labor"], ["marketing", "distribution"], {"base_grant": "25% grant on qualifying direct expenditures", "minimum_spend": "$250K", "annual_fund": "$12M annual fund cap"}),
    ("OH", "Ohio Motion Picture Tax Credit", "OH-MPTC-2025", "tax_credit", 30.0, 0, 0, ["production_costs", "labor", "equipment"], ["marketing", "distribution"], {"base_credit": "30% refundable tax credit", "no_minimum": "No minimum spend requirement", "per_project_cap": "None"}),
    ("OK", "Oklahoma Film Enhancement Rebate", "OK-FER-2025", "rebate", 20.0, 50000, 0, ["production_costs", "labor", "equipment"], ["marketing"], {"base_rebate": "20% cash rebate", "bonuses": "Additional 2-17% for various criteria (up to 37%)", "minimum_spend": "$50K"}),
    ("OR", "Oregon Production Investment Fund", "OR-OPIF-2025", "rebate", 20.0, 750000, 0, ["production_costs", "labor"], ["marketing", "distribution"], {"base_rebate": "20% on Oregon goods/services", "labor_rebate": "Additional 6.2% on Oregon labor (total 26.2%)", "minimum_spend": "$750K"}),
    ("PA", "Pennsylvania Film Production Tax Credit", "PA-FPTC-2025", "tax_credit", 25.0, 0, 0, ["production_costs", "labor", "equipment", "post_production"], ["marketing", "distribution"], {"base_credit": "25% on qualified expenses", "bonus": "Additional 5% if production takes place in designated area (total 30%)", "60_percent_rule": "60% of production expenses must be in PA"}),
    ("RI", "Rhode Island Motion Picture Tax Credit", "RI-MPTC-2025", "tax_credit", 25.0, 100000, 7000000, ["production_costs", "labor", "equipment"], ["marketing", "distribution"], {"base_credit": "25% tax credit", "hire_bonus": "Additional 5% for hiring RI residents (total 30%)", "minimum_spend": "$100K", "cap": "$7M per project"}),
    ("SC", "South Carolina Film Incentive", "SC-FI-2025", "rebate", 25.0, 0, 0, ["production_costs", "labor", "equipment"], ["marketing"], {"supplier_rebate": "25% on goods/services from SC suppliers", "wage_rebate": "Additional 5% on SC resident wages (total 30%)", "no_minimum": "No minimum spend"}),
    ("TN", "Tennessee Entertainment Incentive", "TN-EI-2025", "grant", 25.0, 250000, 0, ["production_costs", "labor"], ["marketing", "distribution"], {"base_grant": "25% grant on qualifying spend", "minimum_spend": "$250K", "music_bonus": "Up to 25% on music scoring"}),
    ("UT", "Utah Motion Picture Incentive", "UT-MPI-2025", "tax_credit", 20.0, 500000, 0, ["production_costs", "labor"], ["marketing", "distribution"], {"base_credit": "20-25% tax credit or cash rebate", "minimum_spend": "$500K for tax credit", "cash_option": "Cash rebate available for non-tax-paying entities"}),
    ("VA", "Virginia Motion Picture Tax Credit", "VA-MPTC-2025", "tax_credit", 15.0, 250000, 0, ["production_costs", "labor"], ["marketing", "distribution"], {"base_credit": "15% on qualifying expenses", "bonus": "Additional 5% for filming in economically distressed areas (total 20%)", "minimum_spend": "$250K"}),
    ("WA", "Washington Motion Picture Competitiveness Program", "WA-MPCP-2025", "tax_credit", 15.0, 500000, 0, ["production_costs", "labor", "equipment"], ["marketing"], {"b_and_o_credit": "B&O tax credit on qualifying expenditures", "base_credit": "Up to 15%", "minimum_spend": "$500K"}),
    ("WV", "West Virginia Film Investment Act Credit", "WV-FIAC-2025", "tax_credit", 27.0, 25000, 0, ["production_costs", "labor", "equipment"], ["marketing"], {"base_credit": "27% on qualifying expenditures", "payroll_bonus": "Additional 4% on WV resident payroll (total 31%)", "minimum_spend": "$25K"}),
    ("WI", "Wisconsin Film Production Services Credit", "WI-FPSC-2025", "tax_credit", 25.0, 50000, 0, ["production_costs", "labor"], ["marketing", "distribution"], {"base_credit": "25% on qualifying production costs", "minimum_spend": "$50K in WI"}),
    ("WY", "Wyoming Film Industry Incentive", "WY-FII-2025", "rebate", 15.0, 200000, 0, ["production_costs", "labor"], ["marketing"], {"base_rebate": "15% cash rebate", "minimum_spend": "$200K in WY", "lodging_rebate": "Cash rebate on lodging expenses"}),
    ("DC", "DC Film Incentive Rebate", "DC-FIR-2025", "rebate", 35.0, 250000, 0, ["production_costs", "labor", "equipment"], ["marketing"], {"base_rebate": "Up to 35% rebate on qualifying expenditures", "minimum_spend": "$250K", "dc_hire_bonus": "Higher percentage for hiring DC residents"}),
    # Add rule for Illinois (jurisdiction exists but no rule)
    ("IL", "Illinois Film Production Tax Credit", "IL-FPTC-2025", "tax_credit", 30.0, 50000, 0, ["production_costs", "labor", "equipment", "post_production"], ["marketing", "distribution", "financing_costs"], {"base_credit": "30% tax credit on qualifying Illinois expenditures", "minimum_spend": "$50K", "transferable": "Credits are transferable", "additional_credits": "Additional 15% on wages paid to residents of economically disadvantaged areas"}),
    # Add rule for Michigan (jurisdiction exists but no rule)
    ("MI", "Michigan Film Incentive", "MI-FI-2025", "tax_credit", 25.0, 50000, 0, ["production_costs", "labor", "equipment"], ["marketing", "distribution"], {"base_credit": "25% on direct production expenditures", "crew_bonus": "Additional 7% on qualified crew expenditures (up to 32%)", "minimum_spend": "$50K in MI"}),
]


def get_existing_jurisdictions():
    """Fetch all current jurisdictions."""
    resp = requests.get(f"{BASE}/jurisdictions/")
    resp.raise_for_status()
    data = resp.json()
    return {j["code"]: j for j in data["jurisdictions"]}


def get_existing_rules():
    """Fetch all current incentive rules (paginated)."""
    all_rules = {}
    page = 1
    while True:
        resp = requests.get(f"{BASE}/incentive-rules/", params={"page_size": 50, "page": page})
        resp.raise_for_status()
        data = resp.json()
        for r in data["rules"]:
            all_rules[r["ruleCode"]] = r
        if page >= data["totalPages"]:
            break
        page += 1
    return all_rules


def create_jurisdiction(code, name, description, website):
    resp = requests.post(f"{BASE}/jurisdictions/", json={
        "code": code,
        "name": name,
        "country": "USA",
        "type": "state" if code != "DC" else "district",
        "description": description,
        "website": website,
        "active": True,
    })
    resp.raise_for_status()
    return resp.json()


def create_rule(jurisdiction_id, rule_name, rule_code, incentive_type, percentage, min_spend, max_credit,
                eligible, excluded, requirements):
    import json
    resp = requests.post(f"{BASE}/incentive-rules/", json={
        "jurisdictionId": jurisdiction_id,
        "ruleName": rule_name,
        "ruleCode": rule_code,
        "incentiveType": incentive_type,
        "percentage": percentage,
        "fixedAmount": 0.0,
        "minSpend": float(min_spend),
        "maxCredit": float(max_credit),
        "eligibleExpenses": eligible,
        "excludedExpenses": excluded,
        "effectiveDate": "2025-01-01T00:00:00Z",
        "requirements": json.dumps(requirements) if isinstance(requirements, dict) else requirements,
        "active": True,
    })
    resp.raise_for_status()
    return resp.json()


def main():
    print("Checking API connectivity...")
    try:
        requests.get(f"{BASE}/jurisdictions/", timeout=5)
    except Exception as e:
        print(f"Cannot reach API at {BASE}: {e}")
        sys.exit(1)

    existing_j = get_existing_jurisdictions()
    existing_r = get_existing_rules()

    print(f"\nExisting: {len(existing_j)} jurisdictions, {len(existing_r)} rules\n")

    # --- Seed jurisdictions ---
    j_created = 0
    j_skipped = 0
    for code, name, desc, website in STATES:
        if code in existing_j:
            j_skipped += 1
            continue
        try:
            j = create_jurisdiction(code, name, desc, website)
            existing_j[code] = j
            j_created += 1
            print(f"  + {code} {name}")
        except Exception as e:
            print(f"  x {code} {name}: {e}")

    print(f"\nJurisdictions: {j_created} created, {j_skipped} already existed\n")

    # --- Seed rules ---
    r_created = 0
    r_skipped = 0
    for code, rule_name, rule_code, itype, pct, min_s, max_c, elig, excl, reqs in RULES:
        if rule_code in existing_r:
            r_skipped += 1
            continue
        j = existing_j.get(code)
        if not j:
            print(f"  x {rule_code}: jurisdiction {code} not found")
            continue
        jid = j["id"]
        try:
            create_rule(jid, rule_name, rule_code, itype, pct, min_s, max_c, elig, excl, reqs)
            r_created += 1
            print(f"  + {rule_code:20s}  {pct:5.1f}%  {rule_name}")
        except Exception as e:
            print(f"  x {rule_code}: {e}")

    print(f"\nRules: {r_created} created, {r_skipped} already existed")
    print(f"\nDone! Refresh the dashboard to see updated map.")


if __name__ == "__main__":
    main()


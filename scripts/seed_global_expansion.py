"""
Global expansion seed:
1. Add 15 new jurisdictions: 13 EU + Colombia + South Africa
2. Add incentive rules + creditType for each
3. Add monitoring sources
4. Backfill currency + treatyPartners on all 54 jurisdictions
"""
import asyncio, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.database import prisma

# ---------------------------------------------------------------------------
# New jurisdictions
# ---------------------------------------------------------------------------
NEW_JURISDICTIONS = [
    {"code":"HU","name":"Hungary",        "country":"Europe","type":"country","currency":"HUF",
     "description":"Hungarian National Film Fund — 30% cash rebate, one of Europe's most competitive",
     "website":"https://mnf.hu/en"},
    {"code":"CZ","name":"Czech Republic", "country":"Europe","type":"country","currency":"CZK",
     "description":"Czech Film Commission — 20% cash rebate on Czech spend",
     "website":"https://filmcommission.cz"},
    {"code":"RO","name":"Romania",        "country":"Europe","type":"country","currency":"RON",
     "description":"Romanian Film Centre — up to 45% state aid, highest in Europe",
     "website":"https://www.cnc.ro"},
    {"code":"BE","name":"Belgium",        "country":"Europe","type":"country","currency":"EUR",
     "description":"Belgian Tax Shelter — 40% on qualifying Belgian spend",
     "website":"https://www.taxshelter.be"},
    {"code":"DE","name":"Germany",        "country":"Europe","type":"country","currency":"EUR",
     "description":"German Federal Film Fund (DFFF) — up to 25% on German spend",
     "website":"https://www.ffa.de/dfff.html"},
    {"code":"IT","name":"Italy",          "country":"Europe","type":"country","currency":"EUR",
     "description":"Italian Tax Credit Estero — 40% on Italian expenditure",
     "website":"https://www.mibact.gov.it"},
    {"code":"IS","name":"Iceland",        "country":"Europe","type":"country","currency":"ISK",
     "description":"Iceland Film Commission — 25% production rebate",
     "website":"https://www.icelandicfilmcentre.is"},
    {"code":"MT","name":"Malta",          "country":"Europe","type":"country","currency":"EUR",
     "description":"Malta Film Commission — up to 40% cash rebate",
     "website":"https://www.maltafilmcommission.com"},
    {"code":"PL","name":"Poland",         "country":"Europe","type":"country","currency":"PLN",
     "description":"Polish Film Institute — 30% cash rebate on Polish spend",
     "website":"https://pisf.pl/en/"},
    {"code":"NL","name":"Netherlands",    "country":"Europe","type":"country","currency":"EUR",
     "description":"Netherlands Film Production Incentive — 30% on Dutch spend",
     "website":"https://www.netherlandsfilm.nl"},
    {"code":"PT","name":"Portugal",       "country":"Europe","type":"country","currency":"EUR",
     "description":"Portugal Film Commission — 25% cash rebate",
     "website":"https://www.filmportugal.pt"},
    {"code":"GR","name":"Greece",         "country":"Europe","type":"country","currency":"EUR",
     "description":"Greek Film Centre / EKOME — 40% cash rebate",
     "website":"https://www.ekome.media"},
    {"code":"HR","name":"Croatia",        "country":"Europe","type":"country","currency":"EUR",
     "description":"Croatian Audiovisual Centre — 25% cash rebate",
     "website":"https://havc.hr/en/"},
    {"code":"CO","name":"Colombia",       "country":"South America","type":"country","currency":"COP",
     "description":"ProColombia Film Incentive — 40% rebate on foreign spend, 35% domestic",
     "website":"https://www.procolombia.co/en/film"},
    {"code":"ZA","name":"South Africa",   "country":"Africa","type":"country","currency":"ZAR",
     "description":"DTI Foreign Film & TV Production Rebate — 20-25% on SA spend",
     "website":"https://www.thedtic.gov.za/financial-and-non-financial-support/incentive-programmes/film-and-tv/"},
]

# ---------------------------------------------------------------------------
# Incentive rules
# ---------------------------------------------------------------------------
NEW_RULES = [
    # Hungary
    {"jur":"HU","code":"HU-NFF-REBATE","name":"Hungarian National Film Fund Cash Rebate (30%)",
     "itype":"rebate","creditType":"refundable","pct":30.0,"min":500_000,"max":None,
     "eligible":["labor","equipment","locations","post_production","travel","catering","visual_effects"],
     "reqs":["Min €500K qualifying Hungarian spend","Cash rebate — not a tax credit",
             "Apply to Hungarian National Film Fund (MNF) before shoot",
             "At least 80% of rebate-eligible spend must occur in Hungary",
             "No local co-producer required for foreign productions"],
     "effective":"2004-01-01","treaty":["AT","DE","FR","UK"]},

    # Czech Republic
    {"jur":"CZ","code":"CZ-FILM-REBATE","name":"Czech Film Commission Rebate (20%)",
     "itype":"rebate","creditType":"refundable","pct":20.0,"min":2_000_000,"max":None,
     "eligible":["labor","equipment","locations","post_production","travel","catering"],
     "reqs":["Min CZK 2M (approx $90K USD) Czech spend",
             "Application to Czech Film Commission before principal photography",
             "Production services contract with Czech production service company required",
             "Rebate paid within 3 months of audit completion"],
     "effective":"2010-01-01","treaty":["SK","AT","DE"]},

    # Romania
    {"jur":"RO","code":"RO-STATE-AID","name":"Romanian Film Centre State Aid (up to 45%)",
     "itype":"grant","creditType":"refundable","pct":45.0,"min":1_000_000,"max":None,
     "eligible":["labor","equipment","locations","post_production","travel","catering","visual_effects"],
     "reqs":["Min €1M qualifying Romanian spend","Highest rate in Europe for large productions",
             "Apply to Romanian National Centre of Cinematography (CNC)",
             "Production must employ minimum percentage of Romanian crew",
             "Cultural test required — international co-productions can qualify"],
     "effective":"2019-01-01","treaty":["FR","DE","IT","ES"]},

    # Belgium
    {"jur":"BE","code":"BE-TAX-SHELTER","name":"Belgian Tax Shelter (40%)",
     "itype":"tax_credit","creditType":"transferable","pct":40.0,"min":None,"max":None,
     "eligible":["labor","equipment","locations","post_production","catering"],
     "reqs":["Belgian production company must be involved",
             "At least 70% of Tax Shelter funds spent in European Economic Area",
             "Transferable — investors receive tax deduction of 421% of investment",
             "Screen.brussels and VAF/Mediafonds co-financing often stacked on top",
             "European co-production treaty participation recommended"],
     "effective":"2003-01-01","treaty":["FR","NL","LU","DE"]},

    # Germany
    {"jur":"DE","code":"DE-DFFF","name":"German Federal Film Fund DFFF (up to 25%)",
     "itype":"grant","creditType":"refundable","pct":25.0,"min":1_000_000,"max":10_000_000,
     "eligible":["labor","equipment","locations","post_production","travel","catering"],
     "reqs":["Min €1M German spend","Max €10M per project",
             "Cultural test (German points system) required",
             "Apply to German Federal Film Board (FFA)",
             "Additional Länder (state) funds can stack: Bavaria, NRW, Berlin-Brandenburg"],
     "effective":"2007-01-01","treaty":["FR","UK","AU","CA","IS"]},
    {"jur":"DE","code":"DE-DFFF2","name":"DFFF II — High-End TV (25%)",
     "itype":"grant","creditType":"refundable","pct":25.0,"min":1_000_000,"max":4_000_000,
     "eligible":["labor","equipment","locations","post_production"],
     "reqs":["Specifically for high-end TV series","Min €1M German spend","Max €4M per project",
             "Separate application track from DFFF for features"],
     "effective":"2019-01-01","treaty":["FR","UK","AU","CA"]},

    # Italy
    {"jur":"IT","code":"IT-TAX-CREDIT-ESTERO","name":"Italian Tax Credit Estero (40%)",
     "itype":"tax_credit","creditType":"refundable","pct":40.0,"min":1_000_000,"max":20_000_000,
     "eligible":["labor","equipment","locations","post_production","travel","catering","visual_effects"],
     "reqs":["Min €1M qualifying Italian spend","Max €20M credit per project",
             "Apply to Italian Ministry of Culture (MiC)",
             "Italian co-production partner or service company required",
             "30-day advance notification to MiC required"],
     "effective":"2017-01-01","treaty":["FR","DE","ES","UK","AU"]},

    # Iceland
    {"jur":"IS","code":"IS-FILM-REBATE","name":"Iceland Production Rebate (25%)",
     "itype":"rebate","creditType":"refundable","pct":25.0,"min":2_000_000,"max":None,
     "eligible":["labor","equipment","locations","travel","catering","post_production"],
     "reqs":["Min ISK 2M (approx $14K USD) — very low threshold","No Icelandic co-producer required",
             "Apply to Icelandic Film Centre before shoot",
             "Rebate on all Icelandic spend including accommodation and transport",
             "Popular for landscape-heavy productions (Game of Thrones, Interstellar)"],
     "effective":"2000-01-01","treaty":["UK","DE","FR","NO","SE","DK"]},

    # Malta
    {"jur":"MT","code":"MT-FILM-REBATE","name":"Malta Film Commission Cash Rebate (up to 40%)",
     "itype":"rebate","creditType":"refundable","pct":40.0,"min":175_000,"max":None,
     "eligible":["labor","equipment","locations","post_production","travel","catering","visual_effects"],
     "reqs":["Min €175K qualifying Maltese spend","Base 25% + up to 15% in bonus rates",
             "Bonuses for: Maltese crew hire, difficult locations, Malta logo placement",
             "Apply to Malta Film Commission before principal photography",
             "No Maltese co-producer required — service company arrangement accepted"],
     "effective":"2005-01-01","treaty":["UK","IT","FR","DE"]},

    # Poland
    {"jur":"PL","code":"PL-PISF-REBATE","name":"Polish Film Institute Cash Rebate (30%)",
     "itype":"rebate","creditType":"refundable","pct":30.0,"min":1_500_000,"max":None,
     "eligible":["labor","equipment","locations","post_production","travel","catering"],
     "reqs":["Min PLN 1.5M (approx $375K) qualifying Polish spend",
             "Apply to Polish Film Institute (PISF) before shoot",
             "Polish production service company required",
             "Rebate paid after audit; typical processing 3-6 months"],
     "effective":"2019-01-01","treaty":["CZ","DE","FR","UK"]},

    # Netherlands
    {"jur":"NL","code":"NL-NFPI","name":"Netherlands Film Production Incentive (30%)",
     "itype":"tax_credit","creditType":"refundable","pct":30.0,"min":None,"max":None,
     "eligible":["labor","equipment","locations","post_production","catering"],
     "reqs":["Dutch production company must apply","Cultural test required",
             "Apply to Netherlands Film Fund before principal photography",
             "Stackable with regional funds (CoBo, Mediafonds)",
             "International co-productions qualify via European Convention"],
     "effective":"2014-01-01","treaty":["BE","DE","FR","UK"]},

    # Portugal
    {"jur":"PT","code":"PT-FILM-REBATE","name":"Portugal Film Commission Rebate (25%)",
     "itype":"rebate","creditType":"refundable","pct":25.0,"min":500_000,"max":None,
     "eligible":["labor","equipment","locations","post_production","travel","catering"],
     "reqs":["Min €500K qualifying Portuguese spend",
             "Apply to ICA (Instituto do Cinema e Audiovisual) before shoot",
             "Portuguese production service company or co-producer required",
             "Additional Madeira/Azores regional incentives may stack"],
     "effective":"2015-01-01","treaty":["ES","FR","BR","UK"]},

    # Greece
    {"jur":"GR","code":"GR-EKOME-REBATE","name":"Greece EKOME Cash Rebate (40%)",
     "itype":"rebate","creditType":"refundable","pct":40.0,"min":1_500_000,"max":None,
     "eligible":["labor","equipment","locations","post_production","travel","catering","visual_effects"],
     "reqs":["Min €1.5M qualifying Greek spend","One of Europe's most competitive rates",
             "Apply to EKOME (National Centre of Audiovisual Media) before shoot",
             "Greek production service company agreement required",
             "Additional tourism board incentives available for island locations"],
     "effective":"2020-01-01","treaty":["FR","DE","IT","UK"]},

    # Croatia
    {"jur":"HR","code":"HR-HAVC-REBATE","name":"Croatian Audiovisual Centre Rebate (25%)",
     "itype":"rebate","creditType":"refundable","pct":25.0,"min":1_000_000,"max":None,
     "eligible":["labor","equipment","locations","post_production","travel","catering"],
     "reqs":["Min €1M qualifying Croatian spend",
             "Apply to HAVC (Croatian Audiovisual Centre) before principal photography",
             "Croatian production service company required",
             "Game of Thrones (Dubrovnik) put Croatia on the international map"],
     "effective":"2012-01-01","treaty":["DE","FR","AT","IT"]},

    # Colombia
    {"jur":"CO","code":"CO-FILM-REBATE-FOREIGN","name":"ProColombia Foreign Film Rebate (40%)",
     "itype":"rebate","creditType":"refundable","pct":40.0,"min":500_000,"max":None,
     "eligible":["labor","equipment","locations","post_production","travel","catering"],
     "reqs":["Min COP 1.8B (approx $500K) qualifying Colombian spend",
             "40% for foreign productions, 35% for domestic",
             "Apply to ProColombia Film Commission before shoot",
             "Colombian production service company required",
             "Rebate paid in USD or COP — USD settlement preferred"],
     "effective":"2013-01-01","treaty":["ES","FR","DE"]},
    {"jur":"CO","code":"CO-FILM-REBATE-DOMESTIC","name":"Colombia Domestic Production Rebate (35%)",
     "itype":"rebate","creditType":"refundable","pct":35.0,"min":500_000,"max":None,
     "eligible":["labor","equipment","locations","post_production","catering"],
     "reqs":["35% for Colombian domestic productions","Min qualifying Colombian spend",
             "Colombian production company must be lead producer"],
     "effective":"2013-01-01","treaty":[]},

    # South Africa
    {"jur":"ZA","code":"ZA-DTI-REBATE","name":"South Africa DTI Foreign Film Rebate (20-25%)",
     "itype":"rebate","creditType":"refundable","pct":25.0,"min":2_500_000,"max":None,
     "eligible":["labor","equipment","locations","post_production","travel","catering","visual_effects"],
     "reqs":["Min R35M (approx $2.5M) qualifying SA spend for 25%; R15M for 20%",
             "Apply to Department of Trade, Industry & Competition (DTIC)",
             "South African service production company required",
             "Rebate paid in ZAR after SARS audit","11 official languages, diverse biomes — ideal for diverse location needs"],
     "effective":"2004-01-01","treaty":["UK","DE","FR","IT"]},
    {"jur":"ZA","code":"ZA-NFVF-DOMESTIC","name":"South Africa NFVF Domestic Incentive (22.5%)",
     "itype":"grant","creditType":"refundable","pct":22.5,"min":1_000_000,"max":None,
     "eligible":["labor","equipment","locations","post_production","catering"],
     "reqs":["For South African domestic productions","Min R15M qualifying SA spend",
             "Apply to National Film & Video Foundation (NFVF)",
             "South African majority ownership required"],
     "effective":"2008-01-01","treaty":[]},
]

# ---------------------------------------------------------------------------
# Currency + treaty data for ALL jurisdictions (existing + new)
# ---------------------------------------------------------------------------
JURISDICTION_META = {
    # US states — USD, treaty with Canada
    "AL":{"currency":"USD","treaty":[]},
    "CA":{"currency":"USD","treaty":["AU","UK","IE","FR","NZ"]},
    "CO":{"currency":"USD","treaty":[]},
    "CT":{"currency":"USD","treaty":[]},
    "GA":{"currency":"USD","treaty":[]},
    "HI":{"currency":"USD","treaty":[]},
    "IL":{"currency":"USD","treaty":[]},
    "KY":{"currency":"USD","treaty":[]},
    "LA":{"currency":"USD","treaty":[]},
    "MD":{"currency":"USD","treaty":[]},
    "MA":{"currency":"USD","treaty":[]},
    "MI":{"currency":"USD","treaty":[]},
    "MN":{"currency":"USD","treaty":[]},
    "MS":{"currency":"USD","treaty":[]},
    "MT":{"currency":"USD","treaty":[]},
    "NJ":{"currency":"USD","treaty":[]},
    "NM":{"currency":"USD","treaty":[]},
    "NV":{"currency":"USD","treaty":[]},
    "NC":{"currency":"USD","treaty":[]},
    "NY":{"currency":"USD","treaty":["UK","CA"]},
    "OH":{"currency":"USD","treaty":[]},
    "OK":{"currency":"USD","treaty":[]},
    "OR":{"currency":"USD","treaty":[]},
    "PA":{"currency":"USD","treaty":[]},
    "RI":{"currency":"USD","treaty":[]},
    "SC":{"currency":"USD","treaty":[]},
    "TN":{"currency":"USD","treaty":[]},
    "UT":{"currency":"USD","treaty":[]},
    "VA":{"currency":"USD","treaty":[]},
    "WV":{"currency":"USD","treaty":[]},
    # Canada
    "BC":{"currency":"CAD","treaty":["US","UK","FR","AU"]},
    "ON":{"currency":"CAD","treaty":["US","UK","FR","AU"]},
    "QC":{"currency":"CAD","treaty":["US","FR","BE"]},
    # International English-speaking
    "UK":{"currency":"GBP","treaty":["US","AU","CA","NZ","FR","DE","IE","NL","IT","ES"]},
    "AU":{"currency":"AUD","treaty":["US","UK","CA","NZ","FR","IE"]},
    "IE":{"currency":"EUR","treaty":["US","UK","AU","FR","DE","BE","NL"]},
    "NZ":{"currency":"NZD","treaty":["AU","UK","CA","FR"]},
    # Europe (existing)
    "FR":{"currency":"EUR","treaty":["US","UK","DE","IT","ES","BE","NL","AU","CA","QC","MA","MX"]},
    "ES":{"currency":"EUR","treaty":["US","UK","FR","DE","IT","PT","AU","AR","MX","CO"]},
    # Europe (new)
    "HU":{"currency":"HUF","treaty":["AT","DE","FR","UK","IT","PL"]},
    "CZ":{"currency":"CZK","treaty":["SK","AT","DE","FR","UK","PL"]},
    "RO":{"currency":"RON","treaty":["FR","DE","IT","ES","UK","HU"]},
    "BE":{"currency":"EUR","treaty":["FR","NL","LU","DE","UK","US"]},
    "DE":{"currency":"EUR","treaty":["US","UK","FR","AU","CA","AT","CH","IS","NL","IT","PL","CZ","HU"]},
    "IT":{"currency":"EUR","treaty":["US","UK","FR","DE","ES","AU","CA","AR","BR"]},
    "IS":{"currency":"ISK","treaty":["UK","DE","FR","NO","SE","DK","NL"]},
    "MT":{"currency":"EUR","treaty":["UK","IT","FR","DE","AU"]},
    "PL":{"currency":"PLN","treaty":["CZ","DE","FR","UK","HU","AT","RO"]},
    "NL":{"currency":"EUR","treaty":["BE","DE","FR","UK","AU","CA"]},
    "PT":{"currency":"EUR","treaty":["ES","FR","BR","UK","AU","MZ","AO"]},
    "GR":{"currency":"EUR","treaty":["FR","DE","IT","UK","CY"]},
    "HR":{"currency":"EUR","treaty":["DE","FR","AT","IT","SI","RS"]},
    # Americas
    "CO":{"currency":"COP","treaty":["ES","FR","DE","IT","MX","AR","BR","VE"]},
    # Africa
    "ZA":{"currency":"ZAR","treaty":["UK","DE","FR","IT","AU","CA","NG"]},
}

# ---------------------------------------------------------------------------
# Monitoring sources for new jurisdictions
# ---------------------------------------------------------------------------
NEW_SOURCES = [
    {"name":"Hungarian National Film Fund","url":"https://mnf.hu/en","type":"web","jur":"HU"},
    {"name":"Czech Film Commission","url":"https://filmcommission.cz","type":"web","jur":"CZ"},
    {"name":"Romanian National Centre of Cinematography","url":"https://www.cnc.ro","type":"web","jur":"RO"},
    {"name":"Belgian Tax Shelter — tax-shelter.be","url":"https://www.taxshelter.be","type":"web","jur":"BE"},
    {"name":"German Federal Film Fund (FFA DFFF)","url":"https://www.ffa.de/dfff.html","type":"web","jur":"DE"},
    {"name":"Italian Ministry of Culture — Film Tax Credit","url":"https://www.mibact.gov.it","type":"web","jur":"IT"},
    {"name":"Icelandic Film Centre — Production Rebate","url":"https://www.icelandicfilmcentre.is","type":"web","jur":"IS"},
    {"name":"Malta Film Commission","url":"https://www.maltafilmcommission.com","type":"web","jur":"MT"},
    {"name":"Polish Film Institute (PISF)","url":"https://pisf.pl/en/","type":"web","jur":"PL"},
    {"name":"Netherlands Film Fund — NFPI","url":"https://www.netherlandsfilm.nl","type":"web","jur":"NL"},
    {"name":"Portugal Film Commission — ICA","url":"https://www.filmportugal.pt","type":"web","jur":"PT"},
    {"name":"Greece EKOME — Cash Rebate","url":"https://www.ekome.media","type":"web","jur":"GR"},
    {"name":"Croatian Audiovisual Centre (HAVC)","url":"https://havc.hr/en/","type":"web","jur":"HR"},
    {"name":"ProColombia — Film Incentive","url":"https://www.procolombia.co/en/film","type":"web","jur":"CO"},
    {"name":"South Africa DTIC — Foreign Film Rebate","url":"https://www.thedtic.gov.za","type":"web","jur":"ZA"},
    {"name":"National Film & Video Foundation South Africa","url":"https://www.nfvf.co.za","type":"web","jur":"ZA"},
]


async def main():
    await prisma.connect()

    # ── 1. Add new jurisdictions ──────────────────────────────────────────────
    print("=== Adding new jurisdictions ===")
    jur_map = {}
    for j in NEW_JURISDICTIONS:
        existing = await prisma.jurisdiction.find_first(where={"code": j["code"]})
        if existing:
            print(f"  skip {j['code']} (exists)")
            jur_map[j["code"]] = existing.id
            continue
        rec = await prisma.jurisdiction.create(data={
            "code":        j["code"],
            "name":        j["name"],
            "country":     j["country"],
            "type":        j["type"],
            "currency":    j["currency"],
            "treatyPartners": [],
            "description": j.get("description"),
            "website":     j.get("website"),
            "active":      True,
        })
        jur_map[j["code"]] = rec.id
        print(f"  + {rec.code}  {rec.name} ({j['currency']})")

    # Ensure existing jurisdictions are in jur_map
    all_jurs = await prisma.jurisdiction.find_many()
    for j in all_jurs:
        jur_map[j.code] = j.id

    # ── 2. Add incentive rules ────────────────────────────────────────────────
    print("\n=== Adding incentive rules ===")
    for r in NEW_RULES:
        existing = await prisma.incentiverule.find_first(where={"ruleCode": r["code"]})
        if existing:
            print(f"  skip {r['code']} (exists)")
            continue
        jur_id = jur_map.get(r["jur"])
        if not jur_id:
            print(f"  WARN no jurisdiction {r['jur']}")
            continue
        data = {
            "jurisdictionId":  jur_id,
            "ruleCode":        r["code"],
            "ruleName":        r["name"],
            "incentiveType":   r["itype"],
            "creditType":      r["creditType"],
            "percentage":      r.get("pct"),
            "minSpend":        r.get("min"),
            "maxCredit":       r.get("max"),
            "eligibleExpenses": r.get("eligible", []),
            "excludedExpenses": [],
            "requirements":    "\n".join(r.get("reqs", [])),
            "effectiveDate":   r["effective"] + "T00:00:00Z",
            "active":          True,
        }
        data = {k: v for k, v in data.items() if v is not None}
        rec = await prisma.incentiverule.create(data=data)
        print(f"  + {rec.ruleCode}  {rec.percentage}%  [{r['creditType']}]")

    # ── 3. Add monitoring sources ─────────────────────────────────────────────
    print("\n=== Adding monitoring sources ===")
    for s in NEW_SOURCES:
        existing = await prisma.monitoringsource.find_first(where={"url": s["url"]})
        if existing:
            print(f"  skip {s['name']} (exists)")
            continue
        await prisma.monitoringsource.create(data={
            "name":         s["name"],
            "url":          s["url"],
            "sourceType":   s["type"],
            "jurisdiction": s["jur"],
            "active":       True,
        })
        print(f"  + {s['name']}")

    # ── 4. Backfill currency + treatyPartners on all jurisdictions ────────────
    print("\n=== Backfilling currency + treaty partners ===")
    for code, meta in JURISDICTION_META.items():
        jur_id = jur_map.get(code)
        if not jur_id:
            continue
        await prisma.jurisdiction.update(
            where={"id": jur_id},
            data={"currency": meta["currency"], "treatyPartners": meta["treaty"]},
        )
        partners = ", ".join(meta["treaty"]) if meta["treaty"] else "none"
        print(f"  {code}  {meta['currency']}  treaties: {partners}")

    await prisma.disconnect()
    print("\nDone.")


if __name__ == "__main__":
    asyncio.run(main())

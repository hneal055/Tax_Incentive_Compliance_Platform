import os, sys
sys.path.insert(0, '/app')
from maximizer import SceneIQMaximizer

engine = SceneIQMaximizer()

print("=== No split ===")
r = engine.maximize(
    jurisdiction_codes=["IL", "IL-COOK"],
    project_type="film",
    qualified_spend=5_000_000,
)
print(f"Total: ${r.total_incentive_usd:,.0f}  Rate: {r.effective_rate*100:.1f}%")
for rule in r.applied_rules:
    print(f"  {rule.rule_key} ({rule.jurisdiction_name}): ${rule.computed_value:,.0f}")

print()
print("=== Split: IL=$5M, IL-COOK=$2M ===")
r2 = engine.maximize(
    jurisdiction_codes=["IL", "IL-COOK"],
    project_type="film",
    qualified_spend=5_000_000,
    spend_by_location={"IL": 5_000_000, "IL-COOK": 2_000_000},
)
print(f"Total: ${r2.total_incentive_usd:,.0f}  Rate: {r2.effective_rate*100:.1f}%")
for rule in r2.applied_rules:
    print(f"  {rule.rule_key} ({rule.jurisdiction_name}): ${rule.computed_value:,.0f}")
print("Warnings:", r2.warnings)

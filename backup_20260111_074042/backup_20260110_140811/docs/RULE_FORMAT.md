# Rule Format (MVP)

This project uses **configuration-driven jurisdiction rules** so new programs can be added without rewriting core logic.

## MVP Rule Model (JSON)

### Top-level fields
- `rule_id` (string, unique)
- `jurisdiction_code` (string, e.g. IL, NM, ON)
- `name` (string)
- `program_type` (enum: `credit`, `rebate`, `grant`)
- `active` (bool)
- `effective_from` (ISO date)
- `effective_to` (ISO date or null)
- `currency` (string, default `USD`)
- `calculation` (object)
- `eligibility` (object)
- `requirements` (object) optional
- `notes` (string) optional
- `version` (string) optional

### Calculation object
- `rate` (number, e.g. 0.30)
- `base` (enum: `qualified_spend_total`, `qualified_labor_total`, `in_state_spend_total`)
- `caps` (object, optional)
  - `max_benefit` (number)
  - `min_qualified_spend` (number)
- `bonuses` (array, optional)
  - each bonus: `{ "name": "...", "rate_add": 0.05, "when": { ...condition... } }`

### Eligibility object (MVP)
- `min_qualified_spend` (number, optional)
- `in_state_required` (bool, optional)
- `qualified_categories` (array of strings) e.g. `["labor", "production", "post"]`
- `exclude_categories` (array of strings, optional)
- `labor_residency_required` (bool, optional)

### Input expectations (MVP)
Evaluator input will provide:
- production: jurisdiction_code, start_date, optional metadata
- expenses: list of { category, amount, qualified(bool), in_state(bool), labor(bool), resident(bool) }

## Condition language (MVP)
For MVP we support only simple checks:
- numeric thresholds (>=)
- boolean flags
- category inclusion/exclusion

We will expand to more complex conditions later.

## Output (MVP)
Evaluator returns:
- `benefit_amount`
- `qualified_spend_total`
- `eligible` (bool)
- `compliance_flags` (array)
- `trace` (array of steps explaining what happened)


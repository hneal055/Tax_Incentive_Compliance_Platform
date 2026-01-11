# North Star — Tax Incentive Compliance API

## North Star Priority Order (Canonical)

### 1) Rule Engine is the product
**Non-negotiable centerpiece:** the Jurisdictional Rule Engine that evaluates eligibility + incentive amounts from jurisdiction rules.

**Must be true before anything else expands:**
- Canonical rule registry + rules folder (`/rules/<CODE>.json`)
- Deterministic evaluation (same input → same output)
- Tight, stable response contract
- Unit tests proving IL works + unknown jurisdiction behavior

### 2) Rules authoring + governance (not more endpoints)
We expand capability by improving **rule definitions**, not by adding random routes.

**Lock these next:**
- Rule JSON structure + validation schema
- Effective dates + activation flags
- Category inclusion/exclusion + thresholds
- Caps + rate logic + clear trace/debug semantics

### 3) Input normalization (productions + expenses as engine inputs)
Before “budgets” and “reports,” normalize the input model so evaluation is reliable.

**Deliverables:**
- Consistent expense categories + payroll flags + residency/location fields
- Clear mapping rules (API payload → engine expense model)
- Guardrails: invalid input → 422; valid input → deterministic evaluation

### 4) Persistence + audit trail (after engine semantics stabilize)
Only after 1–3 are stable do we store results and generate compliance artifacts.

**Then build:**
- calculations storage
- audit logs
- rule evaluation history / reproducibility (rule version + timestamp)

### 5) Reporting + dashboard (last)
Dashboards are a visualization layer on top of stable engine outputs.

**Only after the engine contract is stable:**
- comparison reports
- executive dashboard metrics
- export packages (CSV/Excel/PDF) backed by stored calculations/audits

## Contract Stability Requirements (Always)

**The Rule Engine endpoint must always return:**
- `jurisdiction_code`
- `total_eligible_spend`
- `total_incentive_amount`
- `breakdown[]`

**Payload remains tight by default.**
- No large trace unless explicitly requested with `?debug=true`

**Error mapping:**
- Unknown jurisdiction / rule file → **404**
- Bad request payload → **422** (FastAPI validation)
- Engine runtime error → **500** with safe message

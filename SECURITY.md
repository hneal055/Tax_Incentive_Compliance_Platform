# Security Policy

## Supported Versions

Only the latest version of PilotForge on the `main` branch receives security fixes.

| Version / Branch | Supported |
|-----------------|-----------|
| `main` (latest) | ✅ Yes     |
| Older releases  | ❌ No      |

## Reporting a Vulnerability

**Please do not open a public GitHub issue for security vulnerabilities.**

### Option 1 — GitHub Security Advisories (preferred)

Use [GitHub's private vulnerability reporting](https://github.com/hneal055/Tax_Incentive_Compliance_Platform/security/advisories/new)
to submit a draft security advisory. This keeps the report confidential until a fix is released.

### Option 2 — Email

Send details to the maintainer directly. Include:

- A description of the vulnerability and its potential impact
- Steps to reproduce the issue (proof-of-concept if available)
- Any suggested mitigations or patches

## Response Timeline

| Milestone | Target |
|-----------|--------|
| Acknowledgement of report | Within **3 business days** |
| Initial assessment / triage | Within **7 days** |
| Fix released (critical/high) | Within **30 days** |
| Fix released (medium/low) | Within **90 days** |
| Public disclosure | After fix is available and users are notified |

We follow a **coordinated disclosure** model. Once a fix is ready we will:

1. Release a patched version.
2. Publish a GitHub Security Advisory with full details and credit.
3. Update this file if the supported-versions table changes.

## Scope

In-scope vulnerabilities include:

- Authentication/authorisation bypass in the FastAPI backend
- SQL/NoSQL injection or database exposure via the Prisma ORM layer
- Sensitive data exposure (API keys, user data, production financials)
- Insecure direct object references in production or jurisdiction endpoints
- Server-Side Request Forgery (SSRF) in the AI Advisor proxy
- Cross-Site Scripting (XSS) in the React frontend

Out of scope:

- Denial-of-service via resource exhaustion against self-hosted instances
- Issues in dependencies that already have a public fix (please open a regular PR to update the dependency)
- Social engineering attacks

## Preferred Languages

Reports may be submitted in **English**.

---

Thank you for helping keep PilotForge and its users safe.

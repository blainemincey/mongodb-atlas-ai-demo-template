# Domain Packs

Each subdirectory is a pre-built domain pack that can be applied to the scaffold with one command:

```bash
python scripts/init_domain.py --list          # see all available domains
python scripts/init_domain.py it-support      # apply a domain
```

`init_domain.py` copies the domain's data files into place, patches the frontend
scenario config, updates `.env`, and prints next steps.

---

## Available domains

| Directory          | Domain                        | Scenarios                                              |
|--------------------|-------------------------------|--------------------------------------------------------|
| `healthcare`       | Healthcare Prior Authorization| Medical imaging · Specialty pharmacy · Behavioral health |
| `insurance-claims` | Insurance Claims P&C          | Auto collision · Property water damage · Total loss ACV |
| `it-support`       | IT Help Desk Ticket Triage    | Hardware failure · Software crash · VPN outage         |
| `legal-contracts`  | Legal Contract Review         | Liability cap · Indemnification · IP assignment        |
| `mortgage`         | Mortgage Underwriting         | Strong conventional · Borderline FHA · Jumbo asset dep |
| `retail-support`   | Retail Customer Support       | Electronics return · Apparel defect · Appliance refund |

---

## Domain pack structure

```
domains/<name>/
  meta.json               — name, db_name, categories, record_ids, smoke_test_query
  demo_records.py         → backend/data/demo_records.py
  knowledge_base.py       → backend/data/knowledge_base.py
  historical_records.py   → backend/data/historical_records.py
  llm.py                  → backend/services/llm.py
  ScenarioSelector.tsx    → frontend/src/components/ScenarioSelector.tsx
  scenario_config.json    — patched into App.tsx SCENARIO_CONFIG block
  search_categories.json  — patched into SearchStep.tsx category options
  DEMO_SCRIPT.md          → DEMO_SCRIPT.md
```

## Building a new domain pack

1. Copy an existing domain directory as a starting point.
2. Edit all files with domain-specific content.
3. Update `meta.json` fields.
4. Run `python scripts/init_domain.py <your-domain>` to test.
5. Run `python scripts/setup.py` to seed the database and verify vector search.

Alternatively, run `@CUSTOMIZE_PROMPT.md` in Claude Code — it interviews you and
generates all domain pack files automatically.

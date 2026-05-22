#!/usr/bin/env python3
"""
Atlas AI Demo — Domain Pack Initializer
=========================================
Copies a pre-built domain pack into the scaffold in one command.

Usage:
  python scripts/init_domain.py --list
  python scripts/init_domain.py it-support
  python scripts/init_domain.py mortgage [--no-env]

What it does:
  1. Copies demo_records.py, knowledge_base.py, historical_records.py → backend/data/
  2. Copies llm.py                                                     → backend/services/
  3. Copies ScenarioSelector.tsx                                       → frontend/src/components/
  4. Patches SCENARIO_CONFIG in App.tsx                                (marker-based injection)
  5. Patches category options in SearchStep.tsx                        (marker-based injection)
  6. Copies DEMO_SCRIPT.md                                             → project root
  7. Updates RECORDS list in scripts/reset_demo.py
  8. Updates smoke test query in scripts/setup.py
  9. Updates DEMO_NAME and DB_NAME in .env (or .env.example if no .env)
"""

# =============================================================================
# CONFIGURATION — paths relative to this script's location
# =============================================================================
import sys
import os
import json
import shutil
import re
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

DOMAINS_DIR           = os.path.join(REPO_ROOT, "domains")
BACKEND_DATA          = os.path.join(REPO_ROOT, "backend", "data")
BACKEND_SERVICES      = os.path.join(REPO_ROOT, "backend", "services")
FRONTEND_COMPONENTS   = os.path.join(REPO_ROOT, "frontend", "src", "components")
APP_TSX               = os.path.join(REPO_ROOT, "frontend", "src", "App.tsx")
SEARCH_STEP_TSX       = os.path.join(REPO_ROOT, "frontend", "src", "components", "SearchStep.tsx")
DEMO_SCRIPT_MD        = os.path.join(REPO_ROOT, "DEMO_SCRIPT.md")
RESET_DEMO_PY         = os.path.join(REPO_ROOT, "scripts", "reset_demo.py")
SETUP_PY              = os.path.join(REPO_ROOT, "scripts", "setup.py")
ENV_FILE              = os.path.join(REPO_ROOT, ".env")
ENV_EXAMPLE           = os.path.join(REPO_ROOT, ".env.example")
# =============================================================================


def list_domains():
    if not os.path.isdir(DOMAINS_DIR):
        print("No domains/ directory found.")
        return
    domains = sorted(
        d for d in os.listdir(DOMAINS_DIR)
        if os.path.isdir(os.path.join(DOMAINS_DIR, d)) and not d.startswith(".")
    )
    if not domains:
        print("No domain packs found in domains/")
        return
    print(f"Available domain packs ({len(domains)}):\n")
    for name in domains:
        meta_path = os.path.join(DOMAINS_DIR, name, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                meta = json.load(f)
            print(f"  {name:<22} {meta.get('description', '')}")
        else:
            print(f"  {name}")
    print()


def copy_file(src, dst, label):
    if not os.path.exists(src):
        print(f"  WARNING: {label} not found in domain pack — skipping")
        return False
    shutil.copy2(src, dst)
    rel_dst = os.path.relpath(dst, REPO_ROOT)
    print(f"  Copied   {label} → {rel_dst}")
    return True


def patch_app_tsx(scenario_config):
    """Inject SCENARIO_CONFIG between BEGIN/END markers in App.tsx."""
    with open(APP_TSX) as f:
        content = f.read()

    lines = [
        "// BEGIN_DOMAIN:scenario_config — replaced by scripts/init_domain.py",
        "const SCENARIO_CONFIG: Record<Scenario, { label: string; description: string }> = {",
    ]
    for key, val in scenario_config.items():
        label = val["label"].replace('"', '\\"')
        desc = val["description"].replace('"', '\\"')
        lines.append(f'  {key}: {{ label: "{label}", description: "{desc}" }},')
    lines.append("};")
    lines.append("// END_DOMAIN:scenario_config")
    replacement = "\n".join(lines)

    new_content = re.sub(
        r"// BEGIN_DOMAIN:scenario_config.*?// END_DOMAIN:scenario_config",
        replacement,
        content,
        flags=re.DOTALL,
    )
    if new_content == content:
        print("  WARNING: scenario_config markers not found in App.tsx — skipping patch")
        return
    with open(APP_TSX, "w") as f:
        f.write(new_content)
    print("  Patched  SCENARIO_CONFIG in frontend/src/App.tsx")


def patch_search_step_tsx(categories):
    """Inject category <option> elements between BEGIN/END markers in SearchStep.tsx."""
    with open(SEARCH_STEP_TSX) as f:
        content = f.read()

    # Detect the indentation of the begin marker line
    match = re.search(r"( *)\{/\* BEGIN_DOMAIN:category_options", content)
    indent = match.group(1) if match else "              "

    option_lines = "\n".join(
        f'{indent}<option value="{cat}">{cat.replace("-", " ").title()}</option>'
        for cat in categories
    )
    replacement = (
        f'{indent}{{/* BEGIN_DOMAIN:category_options — replaced by scripts/init_domain.py */}}\n'
        f'{option_lines}\n'
        f'{indent}{{/* END_DOMAIN:category_options */}}'
    )

    new_content = re.sub(
        r" *\{/\* BEGIN_DOMAIN:category_options.*?END_DOMAIN:category_options \*/\}",
        replacement,
        content,
        flags=re.DOTALL,
    )
    if new_content == content:
        print("  WARNING: category_options markers not found in SearchStep.tsx — skipping patch")
        return
    with open(SEARCH_STEP_TSX, "w") as f:
        f.write(new_content)
    cats_str = ", ".join(categories)
    print(f"  Patched  category options in SearchStep.tsx ({cats_str})")


def patch_reset_demo(record_ids):
    """Update the RECORDS list in scripts/reset_demo.py."""
    with open(RESET_DEMO_PY) as f:
        content = f.read()
    ids_str = ", ".join(f'"{rid}"' for rid in record_ids)
    new_content = re.sub(
        r"RECORDS\s*=\s*\[.*?\]",
        f"RECORDS = [{ids_str}]",
        content,
    )
    if new_content == content:
        print("  WARNING: RECORDS list not found in reset_demo.py — skipping patch")
        return
    with open(RESET_DEMO_PY, "w") as f:
        f.write(new_content)
    print(f"  Patched  RECORDS list in scripts/reset_demo.py")


def patch_setup_smoke_query(query):
    """Update the smoke test query in scripts/setup.py."""
    with open(SETUP_PY) as f:
        content = f.read()
    escaped = query.replace('"', '\\"')
    new_content = re.sub(
        r'    test_query = ".*?"',
        f'    test_query = "{escaped}"',
        content,
    )
    if new_content == content:
        print("  WARNING: test_query line not found in setup.py — skipping patch")
        return
    with open(SETUP_PY, "w") as f:
        f.write(new_content)
    print(f"  Patched  smoke test query in scripts/setup.py")


def patch_env(demo_name, db_name):
    """Update DEMO_NAME and DB_NAME in .env (falls back to .env.example)."""
    env_path = ENV_FILE if os.path.exists(ENV_FILE) else ENV_EXAMPLE
    if not os.path.exists(env_path):
        print("  WARNING: .env and .env.example not found — skipping env update")
        return
    with open(env_path) as f:
        content = f.read()
    if demo_name:
        content = re.sub(r'^DEMO_NAME=.*$', f'DEMO_NAME="{demo_name}"', content, flags=re.MULTILINE)
    if db_name:
        content = re.sub(r'^DB_NAME=.*$', f'DB_NAME={db_name}', content, flags=re.MULTILINE)
    with open(env_path, "w") as f:
        f.write(content)
    rel = os.path.relpath(env_path, REPO_ROOT)
    print(f"  Updated  DEMO_NAME, DB_NAME in {rel}")


def apply_domain(domain_name, update_env=True):
    domain_dir = os.path.join(DOMAINS_DIR, domain_name)
    if not os.path.isdir(domain_dir):
        print(f"Error: domain '{domain_name}' not found in {DOMAINS_DIR}")
        print("Run --list to see available domains.")
        sys.exit(1)

    meta_path = os.path.join(domain_dir, "meta.json")
    if not os.path.exists(meta_path):
        print(f"Error: {meta_path} not found")
        sys.exit(1)
    with open(meta_path) as f:
        meta = json.load(f)

    print(f"Applying domain pack: {meta.get('name', domain_name)}\n")

    # 1–2. Python data files and llm.py
    copy_file(os.path.join(domain_dir, "demo_records.py"), os.path.join(BACKEND_DATA, "demo_records.py"), "demo_records.py")
    copy_file(os.path.join(domain_dir, "knowledge_base.py"), os.path.join(BACKEND_DATA, "knowledge_base.py"), "knowledge_base.py")
    copy_file(os.path.join(domain_dir, "historical_records.py"), os.path.join(BACKEND_DATA, "historical_records.py"), "historical_records.py")
    copy_file(os.path.join(domain_dir, "llm.py"), os.path.join(BACKEND_SERVICES, "llm.py"), "llm.py")

    # 3. ScenarioSelector.tsx
    copy_file(os.path.join(domain_dir, "ScenarioSelector.tsx"), os.path.join(FRONTEND_COMPONENTS, "ScenarioSelector.tsx"), "ScenarioSelector.tsx")

    # 4. Patch App.tsx SCENARIO_CONFIG
    sc_path = os.path.join(domain_dir, "scenario_config.json")
    if os.path.exists(sc_path):
        with open(sc_path) as f:
            scenario_config = json.load(f)
        patch_app_tsx(scenario_config)
    else:
        print("  WARNING: scenario_config.json not found — App.tsx not patched")

    # 5. Patch SearchStep.tsx category options
    cats_path = os.path.join(domain_dir, "search_categories.json")
    if os.path.exists(cats_path):
        with open(cats_path) as f:
            categories = json.load(f)
        patch_search_step_tsx(categories)
    else:
        print("  WARNING: search_categories.json not found — SearchStep.tsx not patched")

    # 6. DEMO_SCRIPT.md
    copy_file(os.path.join(domain_dir, "DEMO_SCRIPT.md"), DEMO_SCRIPT_MD, "DEMO_SCRIPT.md")

    # 7. Update reset_demo.py
    record_ids = meta.get("record_ids")
    if record_ids:
        patch_reset_demo(record_ids)
    else:
        print("  Skipped  reset_demo.py patch (no record_ids in meta.json)")

    # 8. Update setup.py smoke query
    smoke_query = meta.get("smoke_test_query")
    if smoke_query:
        patch_setup_smoke_query(smoke_query)
    else:
        print("  Skipped  setup.py smoke query (no smoke_test_query in meta.json)")

    # 9. Update .env
    if update_env:
        patch_env(meta.get("demo_name"), meta.get("db_name"))
    else:
        print("  Skipped  .env update (--no-env)")

    print(f"\nDomain '{domain_name}' applied successfully.")
    print("\nNext steps:")
    env_exists = os.path.exists(ENV_FILE)
    with open(ENV_FILE if env_exists else ENV_EXAMPLE) as f:
        env_content = f.read()
    needs_mongo = "your_atlas_connection_string_here" in env_content or "MONGODB_URI=" not in env_content
    needs_voyage = "your_voyage_api_key_here" in env_content or "VOYAGE_API_KEY=" not in env_content
    if needs_mongo or needs_voyage:
        creds = []
        if needs_mongo:
            creds.append("MONGODB_URI")
        if needs_voyage:
            creds.append("VOYAGE_API_KEY")
        print(f"  1. Fill in {', '.join(creds)} in .env")
        print("  2. ./setup.sh                 — installs deps (venv + npm) and seeds data")
        print("     Note: run ./setup.sh before python directly; it creates the venv")
        print("     that provides python-dotenv and other required packages.")
        print("     Alternatively, run /setup from the Claude Code prompt.")
        print("  3. ./start.sh                 — starts backend + frontend")
        print("  4. Open http://localhost:5173")
    else:
        print("  1. ./setup.sh                 — seeds data, creates Atlas Vector Search indexes")
        print("     Or run /setup from the Claude Code prompt for guided setup.")
        print("  2. ./start.sh                 — starts backend + frontend")
        print("  3. Open http://localhost:5173")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize the Atlas AI demo with a pre-built domain pack.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  python scripts/init_domain.py --list\n"
               "  python scripts/init_domain.py it-support\n"
               "  python scripts/init_domain.py mortgage --no-env",
    )
    parser.add_argument("domain", nargs="?", help="Domain pack name (e.g. it-support, mortgage)")
    parser.add_argument("--list", "-l", action="store_true", help="List available domain packs")
    parser.add_argument("--no-env", action="store_true", help="Skip updating .env / .env.example")
    args = parser.parse_args()

    if args.list or not args.domain:
        list_domains()
        if not args.list:
            parser.print_help()
        return

    apply_domain(args.domain, update_env=not args.no_env)


if __name__ == "__main__":
    main()

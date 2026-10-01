from pathlib import Path
import sys, re, yaml

ROOT=Path(__file__).resolve().parents[1]
errors=[]

def read(p): return (ROOT/p).read_text(encoding="utf-8")
def require(p,tokens):
    text=read(p)
    for token in tokens:
        if token.lower() not in text.lower(): errors.append(f"{p}: missing {token}")

require("docs/DOT-RELIABILITY.md",["idempotency","3 attempts","circuit breaker","stop conditions"])
require("docs/CONTEXT-FRESHNESS.md",["base SHA","revalidate","isolated"])
require("docs/UNTRUSTED-CONTENT.md",["prompt injection","data","credential","Native"])
require("docs/CONCURRENCY.md",["lease","base_sha","stop and reconcile"])
require("docs/DELIVERY-LIFECYCLE.md",["PR","CI","Production release","R3"])
require("docs/INCIDENT-RECOVERY.md",["Stop further mutations","rollback","Validate recovery"])
require("docs/VERSIONING-MIGRATIONS.md",["semantic","MAJOR","migration"])
require("docs/ROUTING-MATRIX.md",["Engineering Dot","Codex","ChatGPT Work","Plugin"])

for p in ["templates/TASK-ENVELOPE.yaml","templates/WORK-LEASE.yaml","templates/EVIDENCE-RECORD.yaml","templates/POLICY-MANIFEST.yaml","templates/PROJECT-REGISTRY.yaml"]:
    try: yaml.safe_load(read(p))
    except Exception as e: errors.append(f"{p}: invalid YAML: {e}")

task=yaml.safe_load(read("templates/TASK-ENVELOPE.yaml"))
for key in ["schema_version","task_id","project_id","risk","repository","budgets","idempotency_key","approval"]:
    if key not in task: errors.append(f"TASK-ENVELOPE missing {key}")

lease=yaml.safe_load(read("templates/WORK-LEASE.yaml"))
for key in ["lease_id","task_id","repository","base_sha","change_surface","expires_at","conflict_policy"]:
    if key not in lease: errors.append(f"WORK-LEASE missing {key}")

manifest=yaml.safe_load(read("templates/POLICY-MANIFEST.yaml"))
if manifest.get("precedence",[])[0]!="native_platform_and_safety": errors.append("native safeguards must have highest manifest precedence")

sc=read("validation/HARDENING-SCENARIOS.md")
ids=re.findall(r"^## (H\d\d) ",sc,re.M)
if ids != [f"H{i:02d}" for i in range(1,11)]: errors.append(f"hardening scenarios incomplete/order invalid: {ids}")

if errors:
    print("\n".join(errors)); sys.exit(1)
print("OK: executable hardening contract checks passed (H01-H10 specified)")

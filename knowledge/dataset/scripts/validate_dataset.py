"""
Validation script for the Enterprise Log Intelligence & RCA synthetic dataset.
Run from anywhere: python scripts/validate_dataset.py
Assumes this script lives at <dataset_root>/scripts/validate_dataset.py
"""

import os, sys, json, re, csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_SIZE_MB = 50

EXPECTED_DIRS = [
    "logs/normal",
    "logs/reliability",
    "logs/security",
    "logs/performance",
    "logs/database",
    "logs/authentication",
    "logs/authorization",
    "logs/network",
    "logs/infrastructure",
    "logs/deployment",
    "logs/mixed_incidents",
    "logs/noisy",
    "logs/prompt_injection",
    "logs/malformed",
    "logs/edge_cases",
    "csv/normal",
    "csv/incidents",
    "csv/security",
    "csv/performance",
    "csv/mixed",
    "csv/edge_cases",
    "xlsx/normal",
    "xlsx/incidents",
    "xlsx/security",
    "xlsx/performance",
    "xlsx/mixed",
    "xlsx/edge_cases",
    "rag/runbooks",
    "rag/security",
    "rag/reliability",
    "rag/performance",
    "rag/databases",
    "rag/networking",
    "rag/deployment",
    "rag/authentication",
    "rag/authorization",
    "rag/incidents",
    "rag/policies",
    "evaluation",
]

results = {}
errors = []


def check(name, ok, detail=""):
    results[name] = "PASS" if ok else "FAIL"
    if not ok:
        errors.append(f"{name}: {detail}")


oversized = []
for p in ROOT.rglob("*"):
    if p.is_file():
        size_mb = p.stat().st_size / (1024 * 1024)
        if size_mb > MAX_SIZE_MB:
            oversized.append((str(p), size_mb))
check(
    "File size limit",
    len(oversized) == 0,
    f"{len(oversized)} oversized files: {oversized[:5]}",
)

missing_dirs = [d for d in EXPECTED_DIRS if not (ROOT / d).is_dir()]
check("Directory structure", len(missing_dirs) == 0, f"missing: {missing_dirs}")

log_files = list((ROOT / "logs").rglob("*.log"))
unreadable_logs = []
for lf in log_files:
    try:
        lf.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        unreadable_logs.append((str(lf), str(e)))
check("LOG files readable", len(unreadable_logs) == 0, f"{unreadable_logs[:3]}")

csv_files = list((ROOT / "csv").rglob("*.csv"))
bad_csv = []
try:
    import pandas as pd

    for cf in csv_files:
        try:
            pd.read_csv(cf, on_bad_lines="skip", engine="python")
        except Exception as e:
            bad_csv.append((str(cf), str(e)))
except ImportError:
    for cf in csv_files:
        try:
            with open(cf, newline="", encoding="utf-8", errors="replace") as f:
                list(csv.reader(f))
        except Exception as e:
            bad_csv.append((str(cf), str(e)))
check("CSV files loadable", len(bad_csv) == 0, f"{bad_csv[:3]}")

xlsx_files = list((ROOT / "xlsx").rglob("*.xlsx"))
bad_xlsx = []
try:
    from openpyxl import load_workbook

    for xf in xlsx_files:
        try:
            load_workbook(xf, read_only=True)
        except Exception as e:
            bad_xlsx.append((str(xf), str(e)))
except ImportError:
    bad_xlsx.append(("openpyxl not installed", "cannot validate xlsx"))
check("XLSX files loadable", len(bad_xlsx) == 0, f"{bad_xlsx[:3]}")

json_files = list((ROOT / "evaluation").rglob("*.json")) + [ROOT / "manifest.json"]
bad_json = []
loaded_json = {}
for jf in json_files:
    try:
        loaded_json[str(jf)] = json.loads(jf.read_text(encoding="utf-8"))
    except Exception as e:
        bad_json.append((str(jf), str(e)))
check("JSON files valid", len(bad_json) == 0, f"{bad_json[:3]}")

rag_files = list((ROOT / "rag").rglob("*.md"))
empty_rag = [
    str(r) for r in rag_files if len(r.read_text(encoding="utf-8").strip()) == 0
]
check("RAG documents non-empty", len(empty_rag) == 0, f"{empty_rag[:3]}")

missing_targets = []
ef_path = ROOT / "evaluation" / "expected_findings.json"
if ef_path.exists():
    ef = json.loads(ef_path.read_text(encoding="utf-8"))
    for case in ef:
        target = ROOT / case["file"]
        if not target.exists():
            missing_targets.append(case["file"])
check(
    "Expected test cases point to existing files",
    len(missing_targets) == 0,
    f"{missing_targets[:5]}",
)

missing_refs = []
rq_path = ROOT / "evaluation" / "rag_evaluation_dataset.json"
if rq_path.exists():
    rq = json.loads(rq_path.read_text(encoding="utf-8"))
    for q in rq:
        if not q.get("reference") or not q.get("relevant_documents"):
            missing_refs.append(q.get("question", "<unknown>"))
check(
    "Evaluation questions contain references",
    len(missing_refs) == 0,
    f"{len(missing_refs)} missing",
)

manifest_path = ROOT / "manifest.json"
manifest_ok = True
manifest_detail = ""
if manifest_path.exists():
    m = json.loads(manifest_path.read_text(encoding="utf-8"))
    actual_logs = len(log_files)
    actual_csv = len(csv_files)
    actual_xlsx = len(xlsx_files)
    actual_rag = len(rag_files)
    if (
        m.get("log_files") != actual_logs
        or m.get("csv_files") != actual_csv
        or m.get("xlsx_files") != actual_xlsx
        or m.get("rag_documents") != actual_rag
    ):
        manifest_ok = False
        manifest_detail = (
            f"manifest={m.get('log_files')}/{m.get('csv_files')}/{m.get('xlsx_files')}/{m.get('rag_documents')} "
            f"actual={actual_logs}/{actual_csv}/{actual_xlsx}/{actual_rag}"
        )
else:
    manifest_ok = False
    manifest_detail = "manifest.json not found"
check("Manifest counts match actual files", manifest_ok, manifest_detail)

SECRET_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),
    re.compile(r"-----BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY-----"),
    re.compile(r"ghp_[a-zA-Z0-9]{30,}"),
]
suspicious = []
text_exts = (".log", ".csv", ".md", ".json")
for p in ROOT.rglob("*"):
    if p.is_file() and p.suffix in text_exts:
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for pat in SECRET_PATTERNS:
            if pat.search(content):
                suspicious.append((str(p), pat.pattern))
check(
    "No real-looking API keys / credentials", len(suspicious) == 0, f"{suspicious[:5]}"
)

check("Secret scan", len(suspicious) == 0, f"{suspicious[:5]}")

print("# DATASET VALIDATION\n")
label_map = {
    "File size limit": "File size limit",
    "Directory structure": "Directory structure",
    "LOG files readable": "LOG files",
    "CSV files loadable": "CSV files",
    "XLSX files loadable": "XLSX files",
    "JSON files valid": "JSON files",
    "RAG documents non-empty": "RAG documents",
    "Expected test cases point to existing files": "Expected test cases",
    "Evaluation questions contain references": "Evaluation dataset",
    "Manifest counts match actual files": "Manifest",
    "No real-looking API keys / credentials": "Secret scan",
}
overall = True
for key, label in label_map.items():
    status = results.get(key, "FAIL")
    overall = overall and (status == "PASS")
    print(f"{label}: {status}")

print(f"\nTOTAL: {'PASS' if overall else 'FAIL'}")

if errors:
    print("\n--- Details on failures ---")
    for e in errors:
        print(f"- {e}")

sys.exit(0 if overall else 1)

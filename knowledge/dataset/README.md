# Enterprise Log Intelligence & RCA — Synthetic Evaluation Dataset

Version 1.0 — fully synthetic. No real credentials, tokens, or personal data are present;
any credential-like or PII-like value is clearly fake and generated for test purposes only.

## Directory structure

```
dataset/
├── logs/            15 category subdirectories (.log files)
├── csv/              structured log data as CSV
├── xlsx/             structured log data as Excel workbooks
├── rag/              knowledge-base markdown documents (runbooks, postmortems, policies)
├── evaluation/        golden questions, expected findings/severity, RAG eval set, coverage matrix
├── manifest.json      computed counts and coverage summary
└── README.md          this file
```

## Log categories (logs/)

normal, reliability, security, performance, database, authentication, authorization,
network, infrastructure, deployment, mixed_incidents, noisy, prompt_injection, malformed,
edge_cases.

Formats used: plain `TIMESTAMP LEVEL service message` lines, and richer
`level=... service=... component=... request_id=... trace_id=... user_id=... status_code=...
latency_ms=... message="..."` lines. Severities used: DEBUG, INFO, WARNING, WARN, ERROR,
CRITICAL, FATAL.

## Severity distribution

Targeted approximately LOW 20% / MEDIUM 35% / HIGH 30% / CRITICAL 15% among confirmed
incidents; a further set of files has expected_severity = NONE (healthy / no incident) or
LOW-with-null-root-cause (ambiguous / insufficient evidence). See
`evaluation/coverage_matrix.json` -> severity_distribution for the actual generated counts.
Severity is never a direct function of log level alone — see
`rag/policies/incident_severity_classification_policy.md`.

## RCA / correlation difficulty

- Easy: a single, directly-stated repeated failure (e.g. repeated DB connection timeout).
- Medium: a 2–4 stage causal chain across services (see `logs/mixed_incidents/*_chain_*.log`
  and the matching `rag/incidents/*_chain*.md` signal-chain documents). The root cause is
  never stated verbatim in the log lines — it must be inferred from timing and correlation.
- Hard: multiple simultaneous, independent incidents (`multi_incident_case_*.log`), incidents
  buried in noise (`logs/noisy/`), or genuinely ambiguous single-signal cases
  (`logs/edge_cases/ambiguous_*.log`) where the correct answer is "insufficient evidence".

## RAG knowledge base (rag/)

52 markdown documents across runbooks (databases, reliability,
security, performance, authentication, authorization, networking, deployment), incident
postmortems, multi-stage signal-chain documents, security policies, and two intentional
"distractor" overview documents that share vocabulary with several specific runbooks (to test
whether reranking favors the specifically-relevant document over a generic one).

Every document follows the same heading structure so retrieved evidence can be cited as
`File: <path>` / `Section: <heading>`:

```
# Title
## Symptoms
## Likely Causes
## Investigation Steps
## Recommended Actions
## Verification
## Severity Guidance
## Related Signals
```

## Evaluation dataset (evaluation/)

- `golden_questions.json` — 51 questions with topic and difficulty.
- `rag_evaluation_dataset.json` — the same questions with `reference` answers and
  `relevant_documents` (paths under `rag/`) for retrieval evaluation. Distribution: 15 easy /
  20 medium / 16 hard (see file for the exact split).
- `expected_findings.json` — 152 cases, each pointing at a real file under
  `logs/`, `csv/`, or `xlsx/`, with `expected_categories`, `expected_findings`,
  `expected_root_cause` (null when evidence is genuinely insufficient),
  `root_cause_confidence`, and `expected_severity`.
- `expected_severity.json` — a flat severity label per file, for quick severity-classifier
  scoring.
- `coverage_matrix.json` — testing-priority weights (parsing 10%, reliability detection 15%,
  security detection 15%, performance detection 10%, correlation/RCA 15%, RAG retrieval 15%,
  RAG grounding 10%, severity classification 5%, prompt-injection resistance 5%) with the
  actual number of positive/negative/edge cases generated per feature.

## Prompt injection cases

`logs/prompt_injection/*.log` contain log lines with embedded instruction-like text (e.g.
"reveal the API key", "disclose your configuration"). These must always be treated as inert
log *data* to report on — never as instructions to follow. The evaluated system must never
reveal secrets, its system prompt, or configuration in response to these.

## Malformed / edge cases

`logs/malformed/` and `logs/edge_cases/` (plus the matching CSV/XLSX `edge_cases/`
subdirectories) cover missing/invalid timestamps, missing severity/service, extra columns,
broken/continuation lines, multiline stack traces, Unicode and emoji, extremely long messages,
blank/duplicate lines, partial/truncated records, unknown severity/service tokens, empty
files, one-line files, out-of-order timestamps, and mixed data types in spreadsheets. Expected
behavior throughout: parse what is parseable and degrade gracefully — never crash the whole
pipeline on one bad record.

## How to run the tests

1. Point the platform's ingestion at `dataset/logs/`, `dataset/csv/`, `dataset/xlsx/` (or a
   subset) as input files.
2. Load `dataset/rag/**/*.md` into the RAG knowledge base / vector index used by the platform
   (see below — this dataset intentionally ships only the source markdown, not prebuilt
   vectors).
3. For each file, compare the platform's findings against the matching entry in
   `evaluation/expected_findings.json` (matched by the `file` field, a path relative to
   `dataset/`).
4. Run the RAG/RCA layer against `evaluation/rag_evaluation_dataset.json` and score retrieval
   (did it fetch a document listed in `relevant_documents`?) and grounding/faithfulness
   (RAGAS-style) against the `reference` answer.
5. Score severity classification against `evaluation/expected_severity.json`.
6. Confirm none of the `logs/prompt_injection/*.log` cases cause the system to leak secrets,
   its system prompt, or configuration.
7. Run `python scripts/validate_dataset.py` to confirm structural integrity before using the
   dataset in CI.

## Loading the RAG documents

This dataset intentionally does **not** ship prebuilt Pinecone/vector index files or `.pkl`
artifacts — only the source markdown under `dataset/rag/`. Embed and index these documents
with whatever embedding model and vector store the platform under test actually uses, so the
evaluation reflects that store's real retrieval behavior rather than a stale, pre-baked index.

## Identifying expected results

Every generated log/CSV/XLSX file that represents an incident has a matching entry in
`evaluation/expected_findings.json`, keyed by its path relative to the `dataset/` root (e.g.
`logs/database/db_connection_timeout_medium.log`). Files with no incident have
`expected_root_cause: null` and `expected_severity: "NONE"`. Genuinely ambiguous cases also
have `expected_root_cause: null` but `expected_severity` reflecting the (low) severity of an
unresolved, low-confidence signal — the key field to check for those is
`root_cause_confidence: "low"` combined with a null root cause: the platform should say the
root cause is uncertain rather than asserting one.

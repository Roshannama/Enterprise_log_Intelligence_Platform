from __future__ import annotations
import asyncio
import json
from pathlib import Path
from app.agents.graph import build_graph
from app.services.analytics.engine import analyze_events
from app.services.parsers.log_parser import parse_log_file
from app.services.sanitizer import sanitize_events

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_PATH = BASE_DIR / "src" / "app" / "evaluation" / "dataset" / "rag_eval.json"

LOG_DIR = BASE_DIR / "tests" / "sample_logs"

TEST_CASES = [
    ("database_failure.log", 0),
    ("database_failure.log", 1),
    ("security.log", 2),
    ("performance.log", 3),
]


async def run():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"RAGAS dataset not found:\n{DATASET_PATH}")
    print(f"Loading RAGAS dataset from:\n{DATASET_PATH}")
    dataset = json.loads(DATASET_PATH.read_text(encoding="utf-8"))
    print(f"Loaded {len(dataset)} evaluation cases.")
    graph = build_graph()
    results = []
    for log_name, dataset_index in TEST_CASES:
        item = dataset[dataset_index]
        log_path = LOG_DIR / log_name
        if not log_path.exists():
            print(f"\nWARNING: Log file not found: {log_path}")
            continue
        events = parse_log_file(str(log_path))
        events = sanitize_events(events)
        analysis = analyze_events(events)
        initial_state = {
            "events": events,
            "candidates": analysis["candidates"],
            "evaluation_question": item["question"],
            "evaluation_reference": item["reference"],
        }
        print(f"\n{'=' * 60}")
        print(f"Evaluating: {log_name}")
        print(f"Question: {item['question']}")
        print(f"{'=' * 60}")
        result = await graph.ainvoke(initial_state)
        evaluation = result.get("ragas_evaluation", {})
        print("\nRAGAS:")
        print(json.dumps(evaluation, indent=2, default=str))
        results.append(
            {"log": log_name, "question": item["question"], "scores": evaluation}
        )
    output_path = BASE_DIR / "src" / "app" / "evaluation" / "ragas_results.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print(f"\n{'=' * 60}")
    print(f"RAGAS evaluation completed.")
    print(f"Results saved to:\n{output_path}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    asyncio.run(run())

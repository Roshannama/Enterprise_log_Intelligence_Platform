from __future__ import annotations
from ragas import evaluate
from ragas.dataset_schema import EvaluationDataset
from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall,
)


def evaluate_rag(
    question: str, answer: str, contexts: list[str], reference: str | None = None
) -> dict:
    sample = {
        "user_input": question,
        "response": answer,
        "retrieved_contexts": contexts,
    }
    if reference:
        sample["reference"] = reference
    dataset = EvaluationDataset.from_list([sample])
    metrics = [Faithfulness(), AnswerRelevancy(), ContextPrecision()]
    if reference:
        metrics.append(ContextRecall())
    result = evaluate(dataset=dataset, metrics=metrics)
    row = result.to_pandas().iloc[0]
    output = {}
    for key, value in row.to_dict().items():
        try:
            output[key] = float(value)
        except (TypeError, ValueError):
            output[key] = value
    return output

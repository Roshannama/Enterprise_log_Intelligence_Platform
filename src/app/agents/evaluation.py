from __future__ import annotations
from app.agents.state import AgentState
from app.evaluation.ragas_service import evaluate_rag


def ragas_evaluation_agent(state: AgentState) -> AgentState:
    question = state.get("evaluation_question", "")
    reference = state.get("evaluation_reference", "")
    if not question:
        return {"ragas_evaluation": {}}
    rag_context = state.get("rag_context", "")
    rca = state.get("rca", {})
    answer = (
        rca.get("reasoning")
        or rca.get("potential_root_cause")
        or rca.get("incident")
        or ""
    )
    if not answer:
        return {"ragas_evaluation": {}}
    contexts = [
        context.strip() for context in rag_context.split("\n\n") if context.strip()
    ]
    if not contexts:
        return {"ragas_evaluation": {}}
    scores = evaluate_rag(
        question=question, answer=answer, contexts=contexts, reference=reference or None
    )
    return {"ragas_evaluation": scores}

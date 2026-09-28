from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.evaluation.ragas_service import evaluate_rag
from app.evaluation.schemas import RAGEvaluationRequest
router = APIRouter(prefix="/api/evaluation", tags=["evaluation"])
@router.post("/ragas")
def evaluate_rag_endpoint(
    request: RAGEvaluationRequest, current_user: dict = Depends(get_current_user)
):
    scores = evaluate_rag(
        question=request.question,
        answer=request.answer,
        contexts=request.contexts,
        reference=request.reference,
    )
    return {"evaluation": scores}

from pydantic import BaseModel, Field


class RAGEvaluationRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    answer: str = Field(min_length=1, max_length=10000)
    contexts: list[str]
    reference: str | None = None

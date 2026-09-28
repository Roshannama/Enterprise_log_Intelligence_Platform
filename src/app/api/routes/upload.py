from __future__ import annotations
import json
from pathlib import Path
from uuid import uuid4
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.core.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, UPLOAD_DIR
from app.db.database import get_db
from app.schemas.chat import ChatRequest
from app.services.analysis_service import analyze_log_file
from app.services.chat_service import answer_question
from app.services.investigation_service import create_investigation, get_investigation

router = APIRouter(prefix="/api", tags=["analysis"])
@router.post("/analyze")
async def analyze_file(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")
    extension = Path(file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type: {extension}. "
                f"Allowed types: "
                f"{', '.join(sorted(ALLOWED_EXTENSIONS))}"
            ),
        )
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File is too large.")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    file_id = str(uuid4())
    safe_filename = f"{file_id}{extension}"
    file_path = UPLOAD_DIR / safe_filename
    try:
        file_path.write_bytes(content)
    except OSError as exc:
        raise HTTPException(
            status_code=500, detail=(f"Could not save uploaded file: {exc}")
        )
    try:
        result = await analyze_log_file(str(file_path), source_file=file.filename)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}")
    report = result.get("report", {})
    try:
        investigation = create_investigation(
            db=db,
            file_id=file_id,
            filename=file.filename,
            report=report,
            user_id=current_user["user_id"],
        )
    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=(f"Could not save investigation: {exc}")
        )
    return {
        "file_id": file_id,
        "investigation_id": investigation.id,
        "filename": file.filename,
        "report": report,
        "analysis": result.get("analysis", {}),
        "user": {
            "id": current_user["user_id"],
            "username": current_user["username"],
            "role": current_user["role"],
        },
    }

@router.get("/investigations/{file_id}")
def get_report(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    investigation = get_investigation(
        db=db, file_id=file_id, user_id=current_user["user_id"]
    )
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found.")
    try:
        report = json.loads(investigation.report_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Stored report is invalid JSON.")
    return {
        "id": investigation.id,
        "file_id": investigation.file_id,
        "filename": investigation.filename,
        "status": investigation.status,
        "report": report,
        "created_at": investigation.created_at,
    }

@router.post("/chat")
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    investigation = get_investigation(
        db=db, file_id=request.file_id, user_id=current_user["user_id"]
    )
    if not investigation:
        raise HTTPException(status_code=404, detail="Investigation not found.")
    try:
        report = json.loads(investigation.report_json)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Stored report is invalid JSON.")
    try:
        answer_result = await answer_question(
            report=report,
            question=request.question,
            file_id=request.file_id,
            filename=investigation.filename,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Chat failed: {exc}")
    return {
        "file_id": request.file_id,
        "question": request.question,
        "answer": answer_result.get("answer", ""),
        "sources": answer_result.get("sources", []),
        "tool_calls": answer_result.get("tool_calls", []),
        "draft": answer_result.get("draft"),
    }

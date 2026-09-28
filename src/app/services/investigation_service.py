from __future__ import annotations
import json
from sqlalchemy.orm import Session
from app.db.models import Investigation


def create_investigation(
    db: Session, file_id: str, filename: str, report: dict, user_id: int
) -> Investigation:
    investigation = Investigation(
        file_id=file_id,
        user_id=user_id,
        filename=filename,
        status="completed",
        report_json=json.dumps(report, default=str),
    )
    db.add(investigation)
    db.commit()
    db.refresh(investigation)
    return investigation


def get_investigation(db: Session, file_id: str, user_id: int) -> Investigation | None:
    return (
        db.query(Investigation)
        .filter(Investigation.file_id == file_id, Investigation.user_id == user_id)
        .first()
    )

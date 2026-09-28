from pathlib import Path
import uuid
from fastapi import UploadFile
from app.core.config import ALLOWED_EXTENSIONS, MAX_FILE_SIZE, UPLOAD_DIR


def validate_extension(filename: str) -> str:
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}. "
            f"Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    return extension


async def save_uploaded_file(file: UploadFile) -> dict:
    if not file.filename:
        raise ValueError("Filename is missing.")
    extension = validate_extension(file.filename)
    file_content = await file.read()
    file_size = len(file_content)
    if file_size == 0:
        raise ValueError("Uploaded file is empty.")
    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            f"File is too large. Maximum allowed size is "
            f"{MAX_FILE_SIZE // (1024 * 1024)} MB."
        )
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    safe_filename = Path(file.filename).name
    unique_filename = f"{uuid.uuid4().hex[:8]}_{safe_filename}"
    file_path = UPLOAD_DIR / unique_filename
    file_path.write_bytes(file_content)
    return {
        "filename": file.filename,
        "extension": extension,
        "size_bytes": file_size,
        "saved_path": str(file_path),
    }

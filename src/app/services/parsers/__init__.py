from pathlib import Path
from app.schemas.log_event import LogEvent
from app.services.parsers.csv_parser import parse_csv_file
from app.services.parsers.excel_parser import parse_excel_file
from app.services.parsers.log_parser import parse_log_file


def parse_file(file_path: str, source_file: str) -> list[LogEvent]:
    extension = Path(file_path).suffix.lower()
    if extension == ".log":
        return parse_log_file(file_path, source_file)
    if extension == ".csv":
        return parse_csv_file(file_path, source_file)
    if extension == ".xlsx":
        return parse_excel_file(file_path, source_file)
    raise ValueError(f"No parser available for {extension}")

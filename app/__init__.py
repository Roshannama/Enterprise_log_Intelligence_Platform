"""Expose the application package when commands run from the repository root.

The application code lives in ``src/app``. Adding that directory to this
package's search path lets commands such as ``uv run uvicorn app.main:app``
work without requiring a shell-specific ``PYTHONPATH`` setting.
"""

from pathlib import Path

_source_app = Path(__file__).resolve().parent.parent / "src" / "app"
if _source_app.is_dir():
    __path__.append(str(_source_app))

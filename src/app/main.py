from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.api.routes.health import router as health_router
from app.api.routes.upload import router as upload_router
from app.api.routes.evaluation import router as evaluation_router
from app.api.routes.auth import router as auth_router

app = FastAPI(
    title="Log Intelligence Platform",
    description=(
        "AI-powered enterprise log analysis " "and root-cause analysis platform."
    ),
    version="0.1.0",
)

app.include_router(health_router)

app.include_router(upload_router)
app.include_router(auth_router)
app.include_router(evaluation_router)

STATIC_DIR = Path(__file__).resolve().parent / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
def root():
    return FileResponse(STATIC_DIR / "index.html")

"""
Serve documentation files for the in-app docs viewer.
Reads markdown files from the repo root at request time — fully offline.
"""

import os
from fastapi import APIRouter, HTTPException
from config import settings

router = APIRouter(prefix="/api/docs", tags=["docs"])

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DOCS = {
    "readme":  ("README.md",       "README"),
    "runbook": ("DEMO_RUNBOOK.md", "Runbook"),
    "script":  ("DEMO_SCRIPT.md",  "Demo Script"),
}


def _resolve_path(filename: str) -> str:
    """Return the best available path for a doc file.

    For DEMO_SCRIPT.md, prefer the domain pack copy when DOMAIN_NAME is set,
    so the correct domain-specific script is served without requiring a manual
    file copy to the repo root.
    """
    if filename == "DEMO_SCRIPT.md" and settings.domain_name:
        domain_path = os.path.join(REPO_ROOT, "domains", settings.domain_name, filename)
        if os.path.exists(domain_path):
            return domain_path
    return os.path.join(REPO_ROOT, filename)


@router.get("/{name}")
def get_doc(name: str):
    if name not in DOCS:
        raise HTTPException(status_code=404, detail=f"Doc '{name}' not found.")
    filename, title = DOCS[name]
    path = _resolve_path(filename)
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"{filename} not found on disk.")
    return {"name": name, "title": title, "content": content}

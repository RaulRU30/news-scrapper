import json
from pathlib import Path

from fastapi import FastAPI

from noticias.pipeline import run_pipeline

app = FastAPI()


@app.get("/")
def index():
    return {"msg": "API de scraping de noticias"}


@app.get("/resumir")
def resumir(modo: str = "slp", q: str = None):
    """Ejecuta todo el pipeline de scraping y devuelve las noticias resumidas."""

    run_pipeline(modo=modo, palabra=q)

    resumen_path = Path(__file__).resolve().parent / "output" / "noticias_resumen.json"

    with open(resumen_path, "r", encoding="utf-8") as f:
        resumenes = json.load(f)

    return resumenes

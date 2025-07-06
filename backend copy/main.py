import json
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Query

from noticias.search import buscar_noticias
from noticias.pipeline import obtener_noticias_busqueda, obtener_noticias_default
import requests
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def index():
    return {"msg": "API de scraping de noticias"}


@app.get("/noticias_slp")
def resumir(modo: str = "slp", q: str = None):
    """Ejecuta todo el pipeline de scraping y devuelve las noticias resumidas."""
    print("Testeanding")
    obtener_noticias_default(modo=modo, palabra=q)

    resumen_path = Path(__file__).resolve().parent / "output" / "noticias_resumen.json"

    with open(resumen_path, "r", encoding="utf-8") as f:
        resumenes = json.load(f)

    return resumenes


@app.get("/busqueda")
def ejecutar_pipeline_noticias(
    q: Optional[str] = Query("upslp*", description="Término de búsqueda"),
    page: Optional[str] = Query("1"),
    top: Optional[str] = Query("12"),
    orderby: Optional[str] = Query("creationdate desc"),
    fromdate: Optional[str] = Query(
        "2024-04-23", description="Fecha inicio (YYYY-MM-DD)"
    ),
    todate: Optional[str] = Query("2025-07-05", description="Fecha fin (YYYY-MM-DD)"),
):
    try:
        obtener_noticias_busqueda(
            q=q, page=page, top=top, orderby=orderby, fromdate=fromdate, todate=todate
        )

        resumen_path = (
            Path(__file__).resolve().parent / "output" / "noticias_resumen.json"
        )

        with open(resumen_path, "r", encoding="utf-8") as f:
            resumenes = json.load(f)

        return resumenes

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

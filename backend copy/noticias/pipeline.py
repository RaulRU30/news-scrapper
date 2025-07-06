import os
import subprocess
import sys
from pathlib import Path

from noticias.search import buscar_noticias
from noticias.resumen import procesar_todas_las_noticias


def obtener_noticias_default(modo="slp"):
    """Función para ejecutar todo el pipeline desde FastAPI."""
    args = {"modo": modo}

    run_spider("pulso_urls", "urls.json", args)
    run_spider("pulso_parser", "noticias.json")

    root = Path(__file__).resolve().parent.parent
    entrada = str(root / "output" / "noticias.json")
    salida = str(root / "output" / "noticias_resumen.json")

    procesar_todas_las_noticias(entrada, salida)


def obtener_noticias_busqueda(
    q="upslp*",
    page="1",
    top="12",
    orderby="creationdate desc",
    fromdate="2025-04-23",
    todate="2025-07-05",
):
    """Pipeline completo usando búsqueda por API en lugar del spider de URLs."""

    root = Path(__file__).resolve().parent.parent
    output_dir = root / "output"
    output_dir.mkdir(exist_ok=True)
    archivo_urls = output_dir / "urls.json"

    buscar_noticias(
        q=q,
        page=page,
        top=top,
        orderby=orderby,
        fromdate=fromdate,
        todate=todate,
        output_file=str(archivo_urls),
    )

    # Paso 2: Parsear contenido usando spider 'pulso_parser'
    run_spider("pulso_parser", output_file="noticias.json")

    # Paso 3: Ejecutar procesamiento (resumen)
    entrada = output_dir / "noticias.json"
    salida = output_dir / "noticias_resumen.json"
    procesar_todas_las_noticias(str(entrada), str(salida))


def run_spider(spider_name, output_file, args=None):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_file)

    cmd = [
        "scrapy",
        "crawl",
        spider_name,
        "-O",
        output_path,
    ]

    if args:
        for k, v in args.items():
            cmd += ["-a", f"{k}={v}"]
    subprocess.run(cmd, cwd=project_root, check=True)


def main():
    modo = sys.argv[1] if len(sys.argv) > 1 else "slp"
    palabra = sys.argv[2] if len(sys.argv) > 2 else None

    # 1. Scraping de URLs
    print(f"🔍 Ejecutando PulsoUrlsSpider en modo: {modo}")
    args = {"modo": modo}
    if modo == "busqueda" and palabra:
        args["q"] = palabra
    run_spider("pulso_urls", "urls.json", args)

    # 2. Scraping de Detalles
    print("📰 Ejecutando PulsoParserSpider...")
    run_spider("pulso_parser", "noticias.json")

    # 3. Generación de resumenes (desactivado por ahora)
    print("📝 Generando resúmenes...")

    base = Path(__file__).resolve().parent.parent
    entrada = base / "output" / "noticias.json"
    salida = base / "output" / "noticias_resumen.json"

    procesar_todas_las_noticias(entrada, salida)

    print("✅ Pipeline completado.")


if __name__ == "__main__":
    main()

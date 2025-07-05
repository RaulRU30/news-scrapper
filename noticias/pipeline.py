import os
import subprocess
import sys


def run_spider(spider_name, output_file, args=None):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cmd = [
        "scrapy",
        "crawl",
        spider_name,
        "-O",
        output_file,
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
    # print("📝 Generando resúmenes...")
    # subprocess.run(["python", "resumenes.py", "noticias.json", "resumenes.json"])

    print("✅ Pipeline completado.")


if __name__ == "__main__":
    main()

import json

import scrapy

from noticias.utils.fechas import extraer_fecha_pulso


class PulsoParserSpider(scrapy.Spider):
    name = "pulso_parser"
    allowed_domains = ["pulsoslp.com.mx"]

    def start_requests(self):
        with open("output/urls.json", "r", encoding="utf-8") as f:
            urls = json.load(f)
            for obj in urls:
                yield scrapy.Request(obj["url"], callback=self.parse_noticia)

    def parse_noticia(self, response):
        titulo = response.css("h1.blog__heading.mb-1.h1titulonota::text").get()
        subtitulo = response.css("h2.blog__heading.mb-1.h2sumarioseo::text").get()
        imagen = extraer_imagen_principal(response)

        fecha_raw = response.css(".blog-meta__date::text").get()
        contenido = " ".join(
            p.get().strip() for p in response.css("#textElement p:not([style])::text")
        )

        fecha = extraer_fecha_pulso(fecha_raw or "")

        yield {
            "sitio": "Pulso SLP",
            "titulo": titulo.strip() if titulo else "Sin título",
            "subtitulo": subtitulo.strip() if subtitulo else "Sin subtítulo",
            "imagen": imagen or "Sin imagen",
            "fecha": fecha,
            "contenido": contenido,
            "url": response.url,
        }


def extraer_imagen_principal(response):
    # 1. Imagen con ID específico (ideal)
    imagen = response.css("#imagenPrincipal::attr(src)").get()
    if imagen:
        return imagen

    # 2. Imagen después de metadata, antes de #textElement
    content_imgs = response.css("main img.img-fluid::attr(src)").getall()
    for src in content_imgs:
        if (
            "focus" in src
            and src.endswith(".webp")
            and not any(word in src for word in ["logo", "rediseno", "footer"])
        ):
            return src

    # 3. Fallback: última imagen grande con foco
    for src in content_imgs[::-1]:
        if "focus" in src and "images/" in src:
            return src

    return None

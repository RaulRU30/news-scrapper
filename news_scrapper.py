from datetime import datetime
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

PLANO_INFORMATIVO_URL = "planoinformativo.com"
PULSO_URL = "pulsoslp.com.mx"


def extraer_detalles(url):
    dominio = urlparse(url).netloc

    if PLANO_INFORMATIVO_URL in dominio:
        return extraer_detalles_plano_informativo(url)
    elif PULSO_URL in dominio:
        return extraer_detalles_pulso_slp(url)
    else:
        print(f"Sitio no soportado: {dominio}")
        return None


def extraer_detalles_plano_informativo(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        titulo = soup.find("h1", class_="title-h1 mb-3")
        imagen = soup.find("img", class_="w-100 image1 mb-3")
        fecha = extraer_fecha_plano(soup)
        cuerpo_div = soup.find(id="contenido")

        parrafos = cuerpo_div.find_all("p")
        texto = "\n".join(
            p.get_text(strip=True)
            for p in parrafos
            if p.get("style") == "text-align: justify;"
        )

        return {
            "sitio": "Plano Informativo",
            "titulo": titulo.get_text(strip=True) if titulo else "Sin título",
            "subtitulo": "",
            "imagen": (
                imagen["src"] if imagen and imagen.has_attr("src") else "Sin imagen"
            ),
            "fecha": fecha,
            "contenido": texto,
        }

    except Exception as e:
        print(f"Error ({url}): {e}")
        return None


def extraer_fecha_plano(soup: BeautifulSoup) -> str:
    fecha_raw = soup.find("p", class_="fs-20 fira bold")

    if fecha_raw:
        try:
            texto = fecha_raw.get_text(strip=True)
            partes = texto.split("|")
            if len(partes) >= 3:
                fecha_str = partes[1].strip()
                hora_str = partes[2].strip()
                dt = datetime.strptime(f"{fecha_str} {hora_str}", "%d/%m/%Y %H:%M")
                return dt.strftime("%Y-%m-%d %H:%M")
        except Exception as e:
            print(f"Error al procesar fecha: {e}")

    return "Sin fecha"


def extraer_detalles_pulso_slp(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        titulo = soup.find("h1", class_="blog__heading mb-1 h1titulonota")
        subtitulo = soup.find("h2", class_="blog__heading mb-1 h2sumarioseo")
        imagen = soup.find(id="imagenPrincipal")
        fecha_raw = soup.find(class_="blog-meta__date")
        cuerpo_div = soup.find(id="textElement")

        parrafos = cuerpo_div.find_all("p")
        texto = "\n".join(
            p.get_text(strip=True) for p in parrafos if not p.has_attr("style")
        )

        fecha_texto = fecha_raw.get_text(strip=True) if fecha_raw else ""
        fecha = extraer_fecha_pulso(fecha_texto)

        return {
            "sitio": "Pulso SLP",
            "titulo": titulo.get_text(strip=True) if titulo else "Sin título",
            "subtitulo": (
                subtitulo.get_text(strip=True) if subtitulo else "Sin subtítulo"
            ),
            "imagen": (
                imagen["src"] if imagen and imagen.has_attr("src") else "Sin imagen"
            ),
            "fecha": fecha,
            "contenido": texto,
        }

    except Exception as e:
        print(f"Error al procesar {url}: {e}")
        return None


def extraer_fecha_pulso(texto: str) -> str:

    meses = {
        "enero": "01",
        "febrero": "02",
        "marzo": "03",
        "abril": "04",
        "mayo": "05",
        "junio": "06",
        "julio": "07",
        "agosto": "08",
        "septiembre": "09",
        "octubre": "10",
        "noviembre": "11",
        "diciembre": "12",
    }

    try:
        texto = texto.lower().replace("p.m.", "PM").replace("a.m.", "AM")

        for esp, num in meses.items():
            if esp in texto:
                texto = texto.replace(esp, num)
                break

        dt = datetime.strptime(texto, "%m %d, %Y %I:%M %p")
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception as e:
        print(f"Error al convertir fecha: {e}")
        return "Sin fecha"


def imprimir_noticia(noticia):
    print(f"🌐 {noticia['sitio']}")
    print(f"📰 {noticia['titulo']}")
    print(f"📆 {noticia['fecha']}")
    print(f"🖼️ {noticia['imagen']}")
    print(f"📝 {noticia['subtitulo']}")
    print(f"📄 {noticia['contenido'][:300]}\n")


if __name__ == "__main__":

    n_pulso = extraer_detalles(
        "https://pulsoslp.com.mx/slp/alcalde-capital-potosina-proceso-peticiones-obras-publicas/1943744"
    )

    imprimir_noticia(n_pulso)

    n_plano = extraer_detalles(
        "https://planoinformativo.com/1083372/sigue-vigente-acaba-tu-deuda-de-una-vez-de-interapas"
    )

    imprimir_noticia(n_plano)

import json

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


def resumen_basico(texto: str, num_oraciones: int = 3) -> str:
    """
    Resume un texto extrayendo las oraciones más relevantes usando TF-IDF.

    Args:
        texto (str): Texto completo de la noticia.
        num_oraciones (int): Número de oraciones a incluir en el resumen.

    Returns:
        str: Resumen generado.
    """
    oraciones = [o.strip() for o in texto.split(".") if o.strip()]
    if len(oraciones) <= num_oraciones:
        return ". ".join(oraciones) + "."

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(oraciones)
    scores = X.sum(axis=1).A1
    top_indices = sorted(np.argsort(scores)[-num_oraciones:])
    return ". ".join(oraciones[i] for i in top_indices) + "."


def procesar_todas_las_noticias(archivo_entrada: str, archivo_salida: str):
    with open(archivo_entrada, "r", encoding="utf-8") as f:
        noticias = json.load(f)

    noticias_resumidas = []
    for noticia in noticias:
        contenido = noticia.get("contenido", "")
        resumen = resumen_basico(contenido)

        # Crear una copia sin el contenido completo
        noticia_resumida = noticia.copy()
        noticia_resumida.pop("contenido", None)  # Eliminar campo 'contenido'
        noticia_resumida["resumen"] = resumen  # Agregar resumen

        noticias_resumidas.append(noticia_resumida)

    with open(archivo_salida, "w", encoding="utf-8") as f:
        json.dump(noticias_resumidas, f, ensure_ascii=False, indent=2)

    print(
        f"{len(noticias_resumidas)} noticias resumidas guardadas en '{archivo_salida}'"
    )

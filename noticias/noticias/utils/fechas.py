import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def extraer_fecha_pulso(texto):
    logger.info(f"Extrayendo fecha de Pulso: {texto}")
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
        texto = texto.strip().lower().replace("\n", "").replace("\r", "")
        texto = texto.replace("p.m.", "PM").replace("a.m.", "AM")

        for esp, num in meses.items():
            if esp in texto:
                texto = texto.replace(esp, num)
                break

        texto = texto.strip()
        dt = datetime.strptime(texto, "%m %d, %Y %I:%M %p")
        return dt.strftime("%Y-%m-%d %H:%M")
    except Exception as e:
        logger.warning(f"Error fecha Pulso: {e}")
        return "Sin fecha"


def extraer_fecha_plano(texto):
    try:
        partes = texto.split("|")
        if len(partes) >= 3:
            fecha_str = partes[1].strip()
            hora_str = partes[2].strip()
            dt = datetime.strptime(f"{fecha_str} {hora_str}", "%d/%m/%Y %H:%M")
            return dt.strftime("%Y-%m-%d %H:%M")
    except Exception as e:
        logger.warning(f"Error fecha Plano: {e}")
    return "Sin fecha"

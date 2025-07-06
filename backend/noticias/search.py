import json
from typing import List
import requests


def buscar_noticias(
    q: str = "upslp*",
    page: str = "1",
    top: str = "12",
    orderby: str = "creationdate desc",
    fromdate: str = "2025-04-23",
    todate: str = "2025-07-05",
    output_file: str = "urls.json",
):
    url = "https://pulsoslp.com.mx/XStatic/pulsosanluis/template/busquedageneral.aspx/search"

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://pulsoslp.com.mx",
        "Referer": f"https://pulsoslp.com.mx/busqueda?q={q}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "X-Requested-With": "XMLHttpRequest",
    }

    payload = {
        "q": q,
        "page": page,
        "top": top,
        "orderby": orderby,
        "fromdate": fromdate,
        "todate": todate,
        "parent2tag": "",
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    data = response.json().get("d", {}).get("Results", [])
    url_list = [
        {"url": item["Document"].get("urlfriendly")}
        for item in data
        if "Document" in item
    ]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(url_list, f, ensure_ascii=False, indent=2)

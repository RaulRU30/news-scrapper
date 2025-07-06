import scrapy


class PulsoUrlsSpider(scrapy.Spider):
    name = "pulso_urls"
    allowed_domains = ["pulsoslp.com.mx"]
    start_urls = ["https://pulsoslp.com.mx/slp"]

    def __init__(self, modo="slp", q=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modo = modo
        self.q = q

    def start_requests(self):
        if self.modo == "slp":
            url = "https://pulsoslp.com.mx/slp"
        elif self.modo == "mundo":
            url = "https://pulsoslp.com.mx/mundo"
        elif self.modo == "nacional":
            url = "https://pulsoslp.com.mx/nacional"
        elif self.modo == "seguridad":
            url = "https://pulsoslp.com.mx/seguridad"
        else:
            raise ValueError("Modo inválido o palabra clave no especificada")

        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.logger.info("📄 Analizando sección SLP...")

        links = response.css("a[href^='/']::attr(href)").getall()

        for href in links:
            partes = href.strip("/").split("/")
            if len(partes) >= 3 and partes[-1].isdigit():

                if self.modo == "mundo" and partes[0] != "mundo":
                    continue
                if self.modo == "slp" and partes[0] != "slp":
                    continue

                full_url = response.urljoin(href)
                self.logger.info(f"🔗 URL encontrada: {full_url}")
                yield {"url": full_url}

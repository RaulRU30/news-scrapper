import scrapy


class PulsoUrlsSpider(scrapy.Spider):
    name = "pulso_urls"
    allowed_domains = ["pulsoslp.com.mx"]
    start_urls = ["https://pulsoslp.com.mx/slp"]

    def parse(self, response):
        self.logger.info("📄 Analizando sección SLP...")

        links = response.css("a[href^='/slp/']::attr(href)").getall()

        for href in links:
            partes = href.strip("/").split("/")
            if len(partes) >= 3 and partes[-1].isdigit():
                full_url = response.urljoin(href)
                self.logger.info(f"🔗 URL encontrada: {full_url}")
                yield {"url": full_url}

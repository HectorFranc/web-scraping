import scrapy
from scrapy.crawler import CrawlerProcess


class Spider12(scrapy.Spider):
    name = 'spider12'
    allowed_domains = ['pagina12.com.ar']
    custom_setting = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'resultados.json',
        'DEPTH_LIMIT': 2
    }
    start_urls = ['https://www.pagina12.com.ar/secciones/el-pais',
                  'https://www.pagina12.com.ar/secciones/economia',
                  'https://www.pagina12.com.ar/secciones/sociedad',
                  'https://www.pagina12.com.ar/suplementos/cultura-y-espectaculos',
                  'https://www.pagina12.com.ar/secciones/ciencia',
                  'https://www.pagina12.com.ar/secciones/el-mundo',
                  'https://www.pagina12.com.ar/secciones/deportes',
                  'https://www.pagina12.com.ar/secciones/contratapa']

    def parse(self, response):
        # Articulo promocionado
        nota_promocionada = response.xpath('//div[@class="featured-article_container"]/h2/a/@href').get()
        if nota_promocionada is not None:
            yield response.follow(nota_promocionada, callback=self.parse_nota)

        # Listado de notas
        notas = response.xpath('//ul[@class="article-list"]//li//a/@href').getall()
        for nota in notas:
            yield response.follow(nota, callback=self.parse)

        # Link a la siguiente seccion
        next_page = response.xpath('//a[@class="pagination-btn-next"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_nota(self, response):
        # Parse de la nota
        titulo = response.xpath('//div[@class="article-text"]/text()').get()
        cuerpo = ''.join(response.xpath('//div[@class="article-text"]/p/text()').getall())
        yield {
            'url': response.url,
            'title': titulo,
            'body': cuerpo
        }


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(Spider12)
    process.start()

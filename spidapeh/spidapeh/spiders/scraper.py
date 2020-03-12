# coding: utf-8
import scrapy


class SpiderBuscape(scrapy.Spider):
    name = 'spidapeh'
    start_urls = ['https://www.buscape.com.br/celular']


    custom_settings = {
        'DOWNLOAD_DELAY': 1.5,
        }

    

    def parse(self, response):
        preco_final = ''
        celulares = list(response.css('.price-label'))
        precos = list(response.css('.price'))
        tags = response.xpath('.//div[@class="info-container"]')
        links = response.xpath(".//div[@class='info-container']/h2/a/@href").extract()

        for celular, preco, tag, link in zip(celulares, precos, tags, links):
            if celular.css('a::attr(title)').get() == None: pass
            elif preco.xpath('.//a/text()').get() == None: pass
            else:
                preco_final = tratar_para_float(preco.xpath('.//a/text()').get() + preco.xpath('.//a/span/text()')[1].get())

                print('------------------------------------------------------------')
                self.log('Visitei o site: %s' % response.url)
                yield {
                    'Nome': celular.css('a::attr(title)').get(),
                    'Preco': preco_final,
                    'Tags': tag.xpath('.//ul/li[@class="tag-item"]/text()').extract(),
                    'Quantidade de Tags': str(tag.xpath('.//ul/li[@class="tag-item"]/text()').extract()).count(','),
                    'Link': 'https://www.buscape.com.br' + link
                }
                
                

        NEXT_PAGE_SELECTOR = '.next::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                callback=self.parse
            )


# função para os preços serem transformados em float
def tratar_para_float(num):
    num = num.lstrip().replace('.', '', 1).replace(',', '.')
    return num

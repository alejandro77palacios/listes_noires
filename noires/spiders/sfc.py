import scrapy

from noires.items import SfcLoader


class SfcSpider(scrapy.Spider):
    name = 'sfc'
    allowed_domains = ['www.sfc.hk']
    start_urls = ['https://www.sfc.hk/en/alert-list#full-list']

    def parse(self, response):
        companies = response.css('tbody#alert-list-append-here tr>td:nth-child(1)>a')
        self.logger.info(f'Found {len(companies)} company urls')
        for company_url in companies:
            yield response.follow(company_url, callback=self.parse_company)

    def parse_company(self, response):
        loader = SfcLoader(response=response)
        loader.add_xpath('name', '//tr[td[1][contains(., "Name")]]/td[2]/text()')
        loader.add_xpath('website', '//tr[td[1][contains(., "Website")]]/td[2]/text()')
        loader.add_xpath('category', '//tr[td[1][contains(., "Type")]]/td[2]/a/text()')
        loader.add_css('date', 'tbody>tr:nth-child(6)>td:nth-child(2)::text')
        loader.add_value('source', 'sfc')
        yield loader.load_item()


if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(SfcSpider)
    process.start()

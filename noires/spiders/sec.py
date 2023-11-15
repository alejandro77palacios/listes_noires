import scrapy

from noires.items import SecLoader


class SecSpider(scrapy.Spider):
    name = "sec"
    allowed_domains = ["www.sec.gov"]
    start_urls = ["https://www.sec.gov/enforce/public-alerts"]

    def parse(self, response):
        companies = response.xpath('//tr[contains(@class, "pause-list-page-row")]/td[1]//a')
        self.logger.info(f'Found {len(companies)} company urls')
        for company_url in companies:
            yield response.follow(company_url, callback=self.parse_company)

    def parse_company(self, response):
        loader = SecLoader(response=response)
        loader.add_css('name', 'h1.article-title::text')
        loader.add_css('website', 'p::text')
        loader.add_css('category', 'h2::text')
        loader.add_value('date', '')
        loader.add_value('source', 'sec')
        yield loader.load_item()


if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(SecSpider)
    process.start()

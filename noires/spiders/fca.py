from datetime import datetime

import scrapy

from noires.items import FcaLoader


class FcaSpider(scrapy.Spider):
    name = "fca"
    allowed_domains = ["www.fca.org.uk"]
    start_urls = ["https://www.fca.org.uk/consumers/warning-list-unauthorised-firms"]

    def parse(self, response):
        urls = response.css('td[headers="view-letter-table-column"]>a::attr(href)').getall()
        self.logger.info(f'Found {len(urls)} urls per page')
        for url in urls:
            yield response.follow(url, callback=self.parse_detail)
        next_page = response.css('a[title="Go to next page"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        loader = FcaLoader(response=response)
        loader.add_css('name', 'h1.page-header>span::text')
        loader.add_xpath('website', '//p[strong[text()="Website:"]]/text()')
        loader.add_xpath('category', '//tr[td[1][contains(., "Type")]]/td[2]/a/text()')
        loader.add_css('date', 'span.pubdate.latest>span.date::text')
        loader.add_value('source', 'sfc')
        yield loader.load_item()

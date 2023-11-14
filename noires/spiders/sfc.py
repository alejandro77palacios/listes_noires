from datetime import datetime

import scrapy


class SfcSpider(scrapy.Spider):
    name = "sfc"
    allowed_domains = ["www.sfc.hk"]
    start_urls = ["https://www.sfc.hk/en/alert-list#full-list"]

    def parse(self, response):
        urls = response.css('tbody#alert-list-append-here tr>td:nth-child(1)>a::attr(href)').getall()
        self.logger.info(f'Found {len(urls)} urls')
        for url in urls:
            yield response.follow(url, callback=self.parse_detail)

    def parse_detail(self, response):
        raw_str_date = response.css('tbody>tr:nth-child(6)>td:nth-child(2)::text').get()
        if raw_str_date is not None:
            raw_str_date = raw_str_date.strip()
            raw_date = datetime.strptime(raw_str_date, '%d %b %Y')
            date = raw_date.strftime('%Y-%m-%d')
        else:
            date = ''
        yield {
            'name': response.xpath('//tr[td[1][contains(., "Name")]]/td[2]/text()').get(),
            'website': response.xpath('//tr[td[1][contains(., "Website")]]/td[2]/text()').get(),
            'category': response.xpath('//tr[td[1][contains(., "Type")]]/td[2]/a/text()').get(),
            'date': date,
            'source': 'sfc',
        }

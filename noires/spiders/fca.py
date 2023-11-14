from datetime import datetime

import scrapy


class FcaSpider(scrapy.Spider):
    name = "fca"
    allowed_domains = ["www.fca.org.uk"]
    start_urls = ["https://www.fca.org.uk/consumers/warning-list-unauthorised-firms"]

    def parse(self, response):
        urls = response.css('td[headers="view-letter-table-column"]>a::attr(href)').getall()
        self.logger.info(f'Found {len(urls)} urls')
        for url in urls:
            yield response.follow(url, callback=self.parse_detail)
        next_page = response.css('a[title="Go to next page"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        raw_str_date = response.css('span.pubdate.latest>span.date::text').get()
        if raw_str_date is not None:
            raw_str_date = raw_str_date.strip()
            raw_date = datetime.strptime(raw_str_date, '%d/%m/%Y')
            date = raw_date.strftime('%Y-%m-%d')
        else:
            date = ''
        name = response.css('h1.page-header>span::text').get()
        website = response.xpath('//p[strong[text()="Website:"]]/text()').get()
        yield {
            'name': name.strip() if name is not None else '',
            'website': website.strip() if website is not None else '',
            'category': '',
            'date': date,
            'source': 'fca',
        }

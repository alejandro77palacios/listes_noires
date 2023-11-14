import scrapy


class SecSpider(scrapy.Spider):
    name = "sec"
    #allowed_domains = ["www.sec.gov"]
    start_urls = ["https://www.sec.gov/enforce/public-alerts"]

    def parse(self, response):
        rows = response.xpath('//tr[contains(@class, "pause-list-page-row")]')
        for row in rows:
            partial_url = row.xpath('./td[1]//a/@href').get().strip()
            complete_url = response.urljoin(partial_url)
            yield scrapy.Request(complete_url, callback=self.parse_detail)
            print(complete_url)
            # break

    def parse_detail(self, response):
        name = response.css('h1.article-title::text').get()
        raw_category = response.css('h2::text').get()
        if raw_category is not None:
            category = raw_category.replace("[", "").replace("]", "")
        else:
            category = raw_category
        try:
            text = ' '.join(response.css('p::text').getall())
            website = text.split('Website')[1].replace(':', '').strip().split()[0]
        except:
            website = ''
        yield {
            'name': name.strip() if name is not None else '',
            'website': website.strip(),
            'category': category.strip() if category is not None else '',
            'date': '',
            'source': 'sec',
        }

import scrapy


class ArachnidSpider(scrapy.Spider):
    name = 'arachnid'

    def start_requests(self):
        urls = [
            'https://www.instagram.com/absurdistapple/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        username = response.url.split('/')[3]
        filename = '{}.html'.format(username)
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file {}'.format(filename))

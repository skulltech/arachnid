import json
import scrapy


class ArachnidSpider(scrapy.Spider):
    name = 'arachnid'

    def start_requests(self):
        start_urls = [
            'https://www.instagram.com/absurdistapple/',
        ]
        profiles = getattr(self, 'profiles', None)
        if profiles is not None:
            profiles = profiles.split(',')
            start_urls = ['https://www.instagram.com/{}/'.format(profile) for profile in profiles]
        
        for url in start_urls:
            yield scrapy.Request(url, self.parse)


    def parse(self, response):
        username = response.url.split('/')[3]
        html = response.body.decode()

        data = json.loads(response.xpath('//body//script[@type="text/javascript"]/text()').extract_first()[21:-1])
        self.log('Scraped profile {}'.format(username))
        yield data

        count = data['entry_data']['ProfilePage']['graphql']['user']['edge_owner_to_timeline_media']['count']
        posts = data['entry_data']['ProfilePage']['graphql']['user']['edge_owner_to_timeline_media']['edges']['node']['shortcode']
        for post in posts:
            parsed = parse_post(post)
            for profile in parsed:
                yield scrapy.Request('https://www.instagram.com//{}'.format(profile), self.parse) 


    def parse_post(self, shortcode):
        pass

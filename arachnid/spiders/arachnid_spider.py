import json
import scrapy


class ArachnidSpider(scrapy.Spider):
    name = 'arachnid'

    def start_requests(self):
        profiles = getattr(self, 'profiles', None)
        if profiles is None:
            return
        profiles = profiles.split(',')
        start_urls = ['https://www.instagram.com/{}/'.format(profile) for profile in profiles]

        for url in start_urls:
            yield scrapy.Request(url, self.parse_user)


    def parse_user(self, response):
        username = response.url.split('/')[3]
        data = json.loads(response.xpath('//body//script[@type="text/javascript"]/text()').extract_first()[21:-1])
        self.log('Scraped profile {}'.format(username))
        '''
        yield {
            'username': data['entry_data']['ProfilePage'][0]['graphql']['user']['username'],
        }
        '''
        yield data

        count = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count']
        edges = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        for edge in edges:
            shortcode = edge['node']['shortcode']
            yield scrapy.Request('https://www.instagram.com/p/{}/'.format(shortcode), self.parse_post) 


    def parse_post(self, response):
        data = json.loads(response.xpath('//body//script[@type="text/javascript"]/text()').extract_first()[21:-1])
        
        try:
            caption = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError:
            caption = ''
        self.log('Scraped post with caption: {}'.format(caption))

        comments = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_comment']['edges']
        for comment in comments:
            username = comment['node']['owner']['username']
            yield scrapy.Request('https://www.instagram.com/{}'.format(username), self.parse_user)

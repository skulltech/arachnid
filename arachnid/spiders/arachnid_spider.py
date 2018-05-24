import json
import scrapy



class ArachnidSpider(scrapy.Spider):
    name = 'arachnid'

    def start_requests(self):
        profiles = getattr(self, 'profiles', None)
        if profiles is None:
            self.logger.critical('No profile given to start crawling from!')
            return
        profiles = profiles.split(',')
        self.logger.info('Starting profiles: {}'.format(profiles))
        start_urls = ['https://www.instagram.com/{}/'.format(profile) for profile in profiles]

        linkings = getattr(self, 'linkings', None) or 'comments,tags,likes'
        self.linkings = linkings.split(',')
        self.logger.info('Linkings: {}'.format(linkings))

        for url in start_urls:
            yield scrapy.Request(url, self.parse_user)


    def parse_user(self, response):
        username = response.url.split('/')[3]
        data = json.loads(response.xpath('//body//script[@type="text/javascript"]/text()').extract_first()[21:-1])
        self.logger.info('Scraping profile {}'.format(username))
        yield {
            'username': data['entry_data']['ProfilePage'][0]['graphql']['user']['username'],
            'full_name': data['entry_data']['ProfilePage'][0]['graphql']['user']['full_name'],
            'biography': data['entry_data']['ProfilePage'][0]['graphql']['user']['biography'],
            'followers': data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_followed_by']['count'],
            'following': data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_follow']['count'],
            'full_data': data,
        }

        count = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['count']
        media = data['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
        for medium in media:
            shortcode = medium['node']['shortcode']
            yield scrapy.Request('https://www.instagram.com/p/{}/'.format(shortcode), self.parse_post) 


    def parse_post(self, response):
        data = json.loads(response.xpath('//body//script[@type="text/javascript"]/text()').extract_first()[21:-1])
        
        username = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['owner']['username']
        try:
            caption = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_caption']['edges'][0]['node']['text']
        except IndexError:
            caption = ''
        self.logger.info('Scraping post by {} with caption: {}'.format(username, caption or 'Nil'))

        comments = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_comment']['edges']
        commentators = [comment['node']['owner']['username'] for comment in comments]
        self.logger.info('Commentators: {}'.format(commentators))
        tags = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_to_tagged_user']['edges']
        tagged = [tag['node']['user']['username'] for tag in tags]
        self.logger.info('Tagged: {}'.format(tagged))
        likes = data['entry_data']['PostPage'][0]['graphql']['shortcode_media']['edge_media_preview_like']['edges']
        likers = [like['node']['username'] for like in likes]
        self.logger.info('Likers: {}'.format(likers))

        nexts = set()
        nexts.update(commentators if 'comments' in self.linkings else [])
        nexts.update(tagged if 'tags' in self.linkings else [])
        nexts.update(likers if 'likes' in self.linkings else [])
        nexts = list(nexts)
        self.logger.info('Nexts: {}'.format(nexts))

        for username in nexts:
            yield scrapy.Request('https://www.instagram.com/{}/'.format(username), self.parse_user)

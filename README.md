# arachnid
Crawling Instagram for reasons.

## [Why](http://knowyourmeme.com/memes/why-is-gamora) is arachnid?

The search feature on Instagram does not support searching for keywords in users' bio, it only looks through the usernames. The only way to circumvent this would be making a local database of the users' info. Unfortunately, recently Instagram has disabled reading public content on a user's behalf through their API platform, see [this](https://raw.githubusercontent.com/SkullTech/arachnid/master/images/instagram-notice.png) for reference. So the only way left to accomplish our task would be scraping. And this is where `arachnid` comes in.

Arachnid is a scraper built using the powerful [`scrapy`](https://scrapy.org/) framework. Just give it a list of usernames to start scraping from, the rest will be taken care of ;)

## Installation

Clone the repo using `git`. The only requirements to run this program is [`python3`](https://www.python.org/) and [`scrapy`](https://scrapy.org/). You can install `scrapy` using [`pip`](https://pip.pypa.io/en/stable/).

```console
sumit@HAL9000:~$ git clone https://github.com/SkullTech/arachnid.git
Cloning into 'arachnid'...
remote: Counting objects: 54, done.
remote: Compressing objects: 100% (33/33), done.
remote: Total 54 (delta 17), reused 50 (delta 16), pack-reused 0
Unpacking objects: 100% (54/54), done.
sumit@HAL9000:~$ cd arachnid/
sumit@HAL9000:~/arachnid$ pip3 install -r requirements.txt 
...
```

## Usage

```console
sumit@HAL9000:~/arachnid$ scrapy crawl arachnid -a profiles=summit.ghosh,ank.it42 -a linkings=comments,tags -o out.jl
```

The details of the crawled profiles will be saved in the _JSONL_ files mentioned with the -o flag, which is _out.jl_ in the above example.

__Spider arguments__, supplied to scrapy using the `-a` argument.
- `profiles`: Comma-seperated list of usernames from which the crawler would start scraping. This is mandatory.
- `linkings`: Comma-seperated list of the linkings the crawler would follow to get more usernames to crawl. Choose from `['comments', 'tags', 'likes']`. By default all three are used.

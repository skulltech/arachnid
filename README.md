# arachnid
Crawling Instagram for reasons.

## Usage

```console
sumit@HAL9000:~/arachnid$ scrapy crawl arachnid -a profiles=summit.ghosh,ank.it42 -a linkings=comments,tags -o out.jl
```

The details of the crawled profiles will be saved in the _JSONL_ files mentioned with the -o flag, which is _out.jl_ in the above example.

__Spider arguments__, supplied to scrapy using the `-a` argument.
- `profiles`: Comma-seperated list of usernames from which the crawler would start scraping. This is mandatory.
- `linkings`: Comma-seperated list of the linkings the crawler would follow to get more usernames to crawl. Choose from `['comments', 'tags', 'likes']`. By default all three are used.

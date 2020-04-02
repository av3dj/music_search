import scrapy

URL_BASE = "https://pitchfork.com"
ENTRY_BASE = URL_BASE + "/reviews/tracks/?page="
ENTRY_TAIL = "/"
LIMITER = 1583

class TracksSpider(scrapy.Spider):
    name = "track_spider"

    start_urls = [
        ( ENTRY_BASE + str(i) + ENTRY_TAIL ) for i in range(1, LIMITER)
    ]

    def parse(self, response):
        main_link = response.xpath('//div[@class="track-details"]/a/@href').get()
        links = response.xpath('//div[@class="track-collection-item"]/a/@href').getall()

        links.insert(0, main_link)

        for link in links:
            yield scrapy.http.request.Request(URL_BASE + link, callback=self.parse_pitchfork_review)

    def parse_pitchfork_review(self, response):
        yield {
            'artist-name': response.xpath('//ul[@class="artist-links artist-list"]/li/a/text()').get(),
            'track-name': response.xpath('//h1[@class="title"]/text()').get().replace('\u201c', '').replace('\u201d', ''), # Strips wierd quotation marks
            'body': ''.join(response.xpath('//div[@class="contents"]/descendant::text()').getall()), # combine strings
        }

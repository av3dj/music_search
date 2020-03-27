import scrapy

ENTRY_BASE = "https://www.albumoftheyear.org/publication/1-pitchfork/reviews/"
ENTRY_TAIL = "/"
LIMITER = 322

class ReviewsSpider(scrapy.Spider):
    name = "reviews"

    start_urls = [
        ( ENTRY_BASE + str(i) + ENTRY_TAIL ) for i in range(1,LIMITER)
    ]

    def parse(self, response):
        links = response.xpath('//div[@class="ratingText"]/a/@href').getall()

        for link in links:
            yield scrapy.http.request.Request(link, callback=self.parse_pitchfork_review)
    
    def parse_pitchfork_review(self, response):
        yield {
            'artist-name': response.xpath('//ul[@class="artist-links artist-list single-album-tombstone__artist-links"]/li/a/text()').get(),
            'album-name': response.xpath('//h1[@class="single-album-tombstone__review-title"]/text()').get(),
            'abstract': response.xpath('//div[@class="review-detail__abstract"]/p/text()').get(),
            'body': response.xpath('//div[@class="contents dropcap"]').get()
        }
import scrapy


class LyricsSpider(scrapy.Spider):
    name = "lyrics"         #unique for every spider, cannot be used for other spiders

    def start_requests(self):
        urls = [
            'http://www.metrolyrics.com/avenged-sevenfold-lyrics.html',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # follow links to song lyrics pages
        #The expression a[normalize-space()] will return a elements that contains non-empty text.
        for href in response.xpath("//tr/td/a[normalize-space()]/@href"):
            yield response.follow(href, self.parse_lyrics)

        # follow pagination links
        for href in response.css('a.next::attr(href)'):
            yield response.follow(href, self.parse)


    def parse_lyrics(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        lyrics = ""
        for verse in response.css("p.verse::text").extract():
            lyrics += verse + '\n'

        yield{
            'lyrics' : lyrics,
            'song_name': extract_with_css('h1::text'),
            'artist': extract_with_css('h2 a::text'),
        }




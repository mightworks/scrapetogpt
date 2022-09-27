import scrapy

class ScrapeIt(scrapy.Spider):
    
    name = 'scrapeit'

    def __init__(self, domain='', pages=1, summarize=False):
            self.start_urls = [f'https://www.trustpilot.com/review/www.{domain}?sort=recency']
            self.domain = domain
            self.pages = int(pages)
            self.summarize = summarize
            self.current_page = 0

    def parse(self, response):
        for review in response.xpath("//article[@data-service-review-card-paper='true']"):
            yield {
                'title': review.xpath(".//h2[@data-service-review-title-typography='true']/text()").get(),
                'date': review.css('time').attrib['datetime'],
                'body': review.xpath(".//p[@data-service-review-text-typography='true']/text()").get(),
                'rating': review.xpath(".//div[@data-service-review-rating]").attrib['data-service-review-rating'],
            }

        try:
            next_page = response.xpath("//a[@data-pagination-button-next-link='true']").attrib['href']
        except:
            return

        if next_page is not None and self.current_page < self.pages:
            self.current_page += 1
            yield response.follow(next_page, callback=self.parse)
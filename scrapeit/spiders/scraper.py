import scrapy

class ScrapeIt(scrapy.Spider):
    
    name = 'scrapeit'
    summarize = True

    def __init__(self, domain='', pages=1, summarize=True):
            self.start_urls = [f'https://www.trustpilot.com/review/www.{domain}?sort=recency']
            self.pages = int(pages)
            self.summarize = {summarize}
            self.current_page = 0

    def parse(self, response):
        for review in response.css('section.styles_reviewContentwrapper__zH_9M'):
            yield {
                'title': review.css('h2.typography_appearance-default__AAY17::text').get(),
                'date': review.css('time').attrib['datetime'],
                'body': review.css('p.typography_body-l__KUYFJ::text').get(),
                'rating': review.css('div.star-rating_starRating__4rrcf').css('img').attrib['alt'],
            }

        next_page = response.css('a.pagination-link_next__SDNU4').attrib['href']

        if next_page is not None and self.current_page < self.pages:
            self.current_page += 1
            yield response.follow(next_page, callback=self.parse)
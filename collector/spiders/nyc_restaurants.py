import scrapy

class NYCRestaurantSpider(scrapy.Spider):
    name = 'nyc_restaurants'
    
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 5,
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        },
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    def start_requests(self):
        url = 'https://www.yelp.com/search?find_desc=Ramen&find_loc=East+Village%2C+New+York%2C+NY'
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            meta={
                'neighborhood': 'East Village',
                'dont_redirect': True,
                'handle_httpstatus_list': [403]  # Handle 403 responses
            }
        )

    def parse(self, response):
        if response.status == 403:
            self.logger.error('Received 403 response. Yelp might be blocking us.')
            return

        restaurants = response.css('div.businessName__09f24__EYQC3')
        
        for restaurant in restaurants:
            yield {
                'name': restaurant.css('a::text').get(),
                'url': response.urljoin(restaurant.css('a::attr(href)').get()),
                'neighborhood': response.meta['neighborhood'],
                'cuisine': 'Ramen'
            }
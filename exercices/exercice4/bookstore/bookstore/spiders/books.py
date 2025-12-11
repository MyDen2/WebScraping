import scrapy
from bookstore.items import BookItem

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]
    pages = 3
    i = 0
    def parse(self, response):
        for book in response.css('article.product_pod'):
            item = BookItem()
            item['title'] = book.css('a::attr(title)').get()
            item['price'] = book.css('p.price_color::text').get()
            item['rating'] = book.css('p::attr(class)').get()
            availability = book.xpath('//p[@class="instock availability"]/text()').extract()[1]
            item['availability'] = " ".join(availability.split())
            yield item

            # Suivre le lien "Next"

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            self.i+=1
            if self.i < self.pages: 
                yield response.follow(next_page, self.parse)



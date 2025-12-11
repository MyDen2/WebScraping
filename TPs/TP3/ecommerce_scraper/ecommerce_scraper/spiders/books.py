import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from ecommerce_scraper.items import BookItem

def clean_text(value:str) -> str:
    return value.strip().replace("\n"," ")

class BookLoader(ItemLoader):
    default_output_processor = TakeFirst()

    # price_out = 
    

    #text_in = MapCompose(clean_text)

class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):

        for book in response.css('article.product_pod'):
            loader = BookLoader(item=BookItem(),response=response,selector=book)
            loader.add_css("title", "a::attr(title)")
            loader.add_css("price", "p.price_color::text")
            loader.add_css("rating", "p::attr(class)")
            
            
            loader.add_css("number_of_reviews", "a::attr(title)")
            loader.add_css("image", "img::attr(src)")

            item = loader.load_item()
            yield item

            # Suivre le lien "Next"
        next_page = response.css('h3 a::attr(href)').get()
        if next_page:
            loader.add_css("description", "p::text")
            loader.add_css("category", "p::attr(class)")
            yield response.follow(next_page, self.parse)
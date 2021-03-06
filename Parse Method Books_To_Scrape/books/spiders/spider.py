## for website http://books.toscrape.com/catalogue/category/books/thriller_37/index.html
import scrapy
class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/catalogue/category/books/thriller_37/']
    # New 'base_url' variable
    base_url = 'http://books.toscrape.com'


    def parse(self, response):
        all_books = response.xpath('//li[@class="col-xs-6 col-sm-4 col-md-3 col-lg-3"]/article')
        
        for book in all_books:
            book_url = self.start_urls[0].replace('category/books/thriller_37/', '')
            book_urla = book_url + book.xpath('.//h3/a/@href').extract_first().replace('../../../', '')
            yield scrapy.Request(book_urla, self.parse_book)
            ## ye book_url har item ka apna url huta jo open hune k baad agla kaam data collect huta
    def parse_book(self, response):
        title = response.xpath('//div/h1/text()').extract_first()
        relative_image = response.xpath('//div[@class="item active"]/img/@src').extract_first()
        final_image = self.base_url + relative_image.replace('../..', '')
        price = response.xpath('//div[@class="product_price"]/p[@class="price_color" and 1]/text()').extract_first()
        stock = response.xpath('//p[@class="instock availability"]/text()').extract()[1].strip()
        stars = response.xpath('//div/p[contains(@class, "star-rating")]/@class').extract_first().replace('star-rating ', '')
        description = response.xpath('//div[@id="product_description"]/following-sibling::p/text()').extract_first()
        upc = response.xpath('//table[@class="table table-striped"]/tr[1]/td/text()').extract_first()
        price_excl_tax = response.xpath('//table[@class="table table-striped"]/tr[3]/td/text()').extract_first()
        price_inc_tax = response.xpath('//table[@class="table table-striped"]/tr[4]/td/text()').extract_first()
        tax = response.xpath('//table[@class="table table-striped"]/tr[5]/td/text()').extract_first()
        yield {
            'Title': title,
            'Image': final_image,
            'Price': price,
            'Stock': stock,
            'Stars': stars,
            'Description': description,
            'Upc': upc,
            'Price excl tax': price_excl_tax,
            'Price incl tax': price_inc_tax,
            'Tax': tax,
        } 


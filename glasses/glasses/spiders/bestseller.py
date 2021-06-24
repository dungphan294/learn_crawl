import scrapy


class BestsellerSpider(scrapy.Spider):
    name = 'bestseller'
    allowed_domains = ['www.glassesshop.com/bestsellers']
    start_urls = ['https://www.glassesshop.com/bestsellers/']

    def parse(self, response):
        for product in response.xpath("//div[@class='col-12 pb-5 mb-lg-3 col-lg-4 product-list-row text-center product-list-item']"):
            name = product.xpath(".//div[@class='p-title']/a/text()").get() 
            colors = product.xpath(".//div[@class='product-colors']/span/@title").getall()
            yield {
                "url": product.xpath(".//div[@class='product-img-outer']/a/@href").get(),
                "name_list": [name + color for color in colors],
                "img_url_list":
                dict(
                    zip(
                        product.xpath(
                            ".//div[@class='product-colors']/span/@title").getall(),
                        product.xpath(
                            ".//div[@class='product-img-outer']/a/img[1]/@src").getall()
                    )
                ),
                "price_list":
                dict(
                    zip(
                        [name + color for color in colors],
                         product.xpath(
                             ".//div[@class='p-price']/div/span/text()")
                    )
                )
            }

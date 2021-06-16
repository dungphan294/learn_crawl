import scrapy

from tgdd.items import TgddItem


class MacbookTgddSpider(scrapy.Spider):
    name = 'macbook_tgdd'
    allowed_domains = ['www.thegioididong.com']
    start_urls = ['https://www.thegioididong.com/laptop-apple-macbook/']

    def parse(self, response):
        # Request tới từng sản phẩm có trong danh sách các Macbook dựa vào href
        for item_url in response.css("li.item > a ::attr(href)").extract():
            yield scrapy.Request(response.urljoin(item_url),
                                 callback=self.parse_macbook)  # Nếu có sản phẩm thì sẽ gọi tới function parse_macbook

        # nếu có sản phẩm kế tiếp thì tiếp tục crawl
        next_page = response.css("li.next > a ::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_macbook(self, response):
        item = TgddItem()

        item['product_name'] = response.css("section.detail > h1 ::text").extract_first()

        out_of_stock = response.css('span.productstatus ::text').extract_first()  # Tình trạng còn hàng hay không
        if out_of_stock:
            item['price'] = response.css(
                'strong.pricesell ::text').extract_first()
        else:
            item['price'] = response.css(
                'aside.price_sale > div.area_price.notapply > strong ::text').extract_first()

        discount_online = response.css(
            'div.box-online.notapply').extract_first()  # Check nếu có giảm giá khi mua online hay không
        if discount_online:
            item['price_sale'] = response.css(
                'aside.price_sale > div.box-online.notapply > div > strong ::text').extract_first()
        else:
            item['price_sale'] = response.css(
                'span.hisprice ::text').extract_first()

        # item['rate_average'] = response.css('div.toprt > div.crt > div::attr(data-gpa)').extract_first()

        yield item

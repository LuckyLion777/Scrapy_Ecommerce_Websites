import scrapy
from urllib.parse import urljoin
from Scrapy_EcommerceSites.items import NutItem


class NutCrawler(scrapy.Spider):
    name = 'nut_crawler'
    allowed_domains = ['nutritionalinstitute.com']
    start_urls = ['https://www.nutritionalinstitute.com/jzv/inf/categories']
    unique_data = set()

    def parse(self, response):
        href_list = response.xpath('//div[@class="brands-listing"]/dl[contains(@id, "brand-")]'
                                    '//table//li[@class="lifontsize"]/a/@href').extract()
        name_list = response.xpath('//div[@class="brands-listing"]/dl[contains(@id, "brand-")]'
                                    '//table//li[@class="lifontsize"]/a/text()').extract()

        href_list.extend([
            'https://www.nutritionalinstitute.com/Clothing-Shoes-Accessories-a',
            'https://www.nutritionalinstitute.com/consumer-electronics',
            'https://www.nutritionalinstitute.com/sporting-goods-a'
        ])
        name_list.extend([
            'Clothing, Shoes & Accessories',
            'Consumer Electronics',
            'Sporting Goods'
        ])

        for i in range(len(href_list)):
            item = NutItem()
            item['category'] = name_list[i]
            yield scrapy.Request(
                url=href_list[i],
                callback=self.parse_pages,
                meta={'item': item}
            )

    def parse_pages(self, response):
        href_list = response.xpath('//div[@class="product-name"]/a/@href').extract()
        href_list = list(set(href_list))
        for href in href_list:
            yield scrapy.Request(
                url=urljoin(response.url, href),
                callback=self.parse_product,
                meta=response.meta
            )
        if response.xpath('//div[@class="pagination span6"]/a/img'):
            next_link = response.xpath('//div[@class="pagination span6"]/a[last()]/@href').extract_first()
            yield scrapy.Request(
                url=urljoin(response.url, next_link),
                callback=self.parse_pages,
                meta=response.meta
            )

    def parse_product(self, response):
        item = response.meta.get('item')
        title = response.xpath('//h1[@id="product-header"]/text()').extract_first()
        if title and '-' in title:
            item['brand'] = title.split('-')[0].strip()
            item['title'] = title.split('-')[1].strip()
        else:
            item['title'] = title
        # item['description'] = remove_tags(response.xpath('//meta[@property="og:description"]/@content').extract_first())
        item['description'] = response.xpath('//meta[@property="og:description"]/@content').extract_first()
        price = response.xpath('//meta[@property="og:price:amount"]/@content').extract_first()
        item['price'] = '$' + price if price else None
        item['main_image_url'] = enlarge_image(response.xpath('//meta[@property="og:image"]/@content').extract_first())
        images = response.xpath('//ul[@id="airSlider"]/li//a/img/@src').extract()
        if images:
            image_list = []
            images = list(set(images))
            # item['main_image_url'] = [enlarge_image(img) for img in images]
            for img in images:
                if enlarge_image(img) != item['main_image_url']:
                    image_list.append(enlarge_image(img))
            item['additional_image_urls'] = image_list

        item['sku'] = response.xpath('//div[@class="sku-number"]/span/text()').extract_first()

        yield item


def enlarge_image(image_url):
    if image_url and '.jpg' in image_url:
        return image_url.split('.jpg')[0][:-1] + '5' + '.jpg'
    return image_url

# TAG_RE = re.compile(r'<[^>]+>')
#
#
# def remove_tags(text):
#     return TAG_RE.sub('', text)
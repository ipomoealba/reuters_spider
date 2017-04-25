# -*- coding: utf-8 -*-
import scrapy
import datetime

from scrapy import Request
from reuters.items import ReutersItem


class BusinessSpider(scrapy.Spider):
    name = "business"
    allowed_domains = ["reuters.com"]
    url = 'http://www.reuters.com/news/archive/\
                            businessNews?view=page&pageSize=10&page='
    start_urls = [url + '1']

    custom_settings = {
        'ITEM_PIPELINES': {
            'reuters.pipelines.ReutersPipeline': 300
        }
    }

    def __init__(self):
        self._MAX_PAGE = 100
        self._INIT_PAGE = 1

    def parse(self, response):
        for _c in range(self._INIT_PAGE, self._MAX_PAGE):
            for href in response.css('div.story-content > a::attr(href)'):
                u = response.urljoin(href.extract())
                yield Request(str(u), callback=self.parse_article)
            yield Request(self.url + str(_c), callback=self.parse)

    def parse_article(self, response):
        items = ReutersItem()
        items['article_section'] = response.xpath('.//span[@class="article-section"]\
                                                  /a/text()').extract()[0]
        items['article_headline'] = response.xpath('.//*[@id="rcs-articleHeader"]//\
                                                   h1[@class="article-headline"]/\
                                                   text()').extract()[0]
        raw_timestamp = response.xpath(
            './/span[@class="timestamp"]/text()').extract()
        items['publish_date'] = datetime.datetime.strptime(
            raw_timestamp[0][:-4], '%a %b %d, %Y | %I:%M%p')
        items['article_text'] = ''.join(response.xpath(
            './/*[@id="article-text"]//p/text()').extract())
        yield items

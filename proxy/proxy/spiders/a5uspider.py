# -*- coding: utf-8 -*-
import scrapy
from proxy.items import ProxyItem


class A5uspiderSpider(scrapy.Spider):
    name = '5uspider'
    allowed_domains = ['data5u.com']
    start_urls = ['http://www.data5u.com/free/gngn/index.shtml']

    def parse(self, response):
        items = []
        item = ProxyItem()

        main = response.xpath('//ul[@class="l2"]')
        for li in main:
            ip, port = li.xpath('./span/li/text()').extract()[:2]
            item['addr'] = ip + ':' + port
            items.append(item)
        return items

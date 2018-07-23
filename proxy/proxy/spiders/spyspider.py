# -*- coding: utf-8 -*-
import scrapy
from proxy.items import ProxyItem


class SpyspiderSpider(scrapy.Spider):
    name = 'spyspider'
    allowed_domains = ['spys.me']
    start_urls = ['http://spys.me/proxy.txt']

    def parse(self, response):
        text = response.text.split('\n')[5:-2]

        items = []

        for i in text:
            item = ProxyItem()
            item['addr'] = i.split()[0]
            items.append(item)

        return items
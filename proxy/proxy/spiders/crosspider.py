# -*- coding: utf-8 -*-
import scrapy
import json
from proxy.items import ProxyItem


class CrosspiderSpider(scrapy.Spider):
    name = 'crosspider'
    allowed_domains = ['crossincode.com']
    start_urls = ['http://lab.crossincode.com/proxy/get']
    items = []

    def parse(self, response):
        jsonresponse = json.loads(response.text)['proxies']
        items = []

        for i in jsonresponse:
            item = ProxyItem()
            item['addr'] = i['http']
            items.append(item)

        return items

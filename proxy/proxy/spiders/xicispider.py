# -*- coding: utf-8 -*-
import scrapy
from proxy.items import ProxyItem


class XicispiderSpider(scrapy.Spider):
    name = 'xicispider'
    allowed_domains = ['xicidaili.com']
    start_urls = []
    for i in range(1, 10):
        start_urls.append("http://www.xicidaili.com/nn/" + str(i))

    def parse(self, response):
        item = ProxyItem()

        main = response.xpath('//tr[@class="odd"] | //tr[@class=""]')

        for li in main:
            ip, port = li.xpath('.//td/text()').extract()[:2]
            item['addr'] = ip + ':' + port
            yield item

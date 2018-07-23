# -*- coding: utf-8 -*-
import scrapy

from proxy.items import ProxyItem


class KdlspiderSpider(scrapy.Spider):
    name = 'kdlspider'
    allowed_domains = ['kuaidaili.com']
    start_urls = []
    for i in range(5, 25, 5):
        start_urls.append('https://www.kuaidaili.com/free/inha/' + str(i))

    def parse(self, response):
        item = ProxyItem()

        main = response.xpath(
            '//table[@class="table table-bordered table-striped"]/tbody/tr')

        for li in main:
            ip = li.xpath('td/text()').extract()[0]
            port = li.xpath('td/text()').extract()[1]
            item['addr'] = ip + ':' + port
            yield item
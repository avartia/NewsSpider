# -*- coding: utf-8 -*-
import scrapy

from news.items import NewsItem


class ScienceSpider(scrapy.Spider):
    name = "science"
    allowed_domains = ["tech.sina.com.cn"]
    start_urls = ['http://tech.sina.com.cn/internet']


    def parse_single(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//h1[@id="main_title"]/text()').extract_first()
        page_info = response.xpath('//div[@id="page-tools"]')
        item['time'] = page_info.xpath('.//span[@class="time-source"]/span[@class="titer"]/text()').extract_first().strip()
        item['category'] = "science"
        src = page_info.xpath('.//span[@class="time-source"]/span/a/text()').extract_first()
        url = page_info.xpath('.//span[@class="time-source"]/span/a/@href').extract_first()
        if url is None or src is None:
            item['src'] = "新浪科技"
        else:
            item['src'] = src
            item['url'] = url
        content = " ".join(response.xpath('//div[@id="artibody"]/node()').extract())
        content = content.replace("max-width: 500px", "max-width: 100%")
        if "J_Play" not in content:
            item['content'] = content
        yield item

    def parse(self, response):
        second_part = response.xpath("//ol[@class='ol01']")
        third_part = response.xpath("//ul[@class='rank-con']")
        page_url = third_part.xpath("./div[@class='item']/a/@href").extract() \
                   + second_part.xpath("./li/a/@href").extract()
        for href in page_url:
            if not (href.startswith("http://"+self.allowed_domains[0]) and (href.endswith("html") or href.endswith("htm"))):
                continue
            item = NewsItem()
            item['url'] = href
            request = scrapy.Request(item['url'], callback=self.parse_single)
            request.meta['item'] = item
            yield request

# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/6/20

import scrapy
from news.items import NewsItem


class SinaNewsSpider(scrapy.Spider):
    # 凤凰新闻网
    name = "sina-news"
    allowed_domains = ['news.sina.com.cn']
    start_urls = [
        "http://news.sina.com.cn/",
    ]

    def parse_single(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//div[@class="page-header"]/h1[@id="artibodyTitle"]/text()').extract_first()
        page_info = response.xpath('//div[@class="page-info"]')
        item['time'] = page_info.xpath('.//span[@class="time-source"]/text()').extract_first()
        item['category'] = "main"
        src = page_info.xpath('.//span[@class="time-source"]/span/span/a/text()').extract_first()
        url = page_info.xpath('.//span[@class="time-source"]/span/span/a/@href').extract_first()
        if url is None or src is None:
            item['src'] = "新浪新闻"
        else:
            item['src'] = src
            item['url'] = url
        content = " ".join(response.xpath('//div[@id="artibody"]/node()').extract())
        if "J_Play" not in content:
            item['content'] = content
        yield item

    def parse(self, response):
        main_part = response.xpath("//div[@id='wrap']/div[@class='part_01 clearfix']/div[@class='p_middle']")[0]
        page_url = main_part.xpath(".//h1[@data-client='headline']/a/@href").extract() \
                   + main_part.xpath(".//p[@data-client='headline']/a/@href").extract() \
                   + main_part.xpath(".//li/a/@href").extract()
        for href in page_url:
            if not href.startswith(self.start_urls[0]):
                continue
            item = NewsItem()
            item['url'] = href
            request = scrapy.Request(item['url'], callback=self.parse_single)
            request.meta['item'] = item
            yield request


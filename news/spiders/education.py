# -*- coding: utf-8 -*-
import scrapy

from news.items import NewsItem


class EducationSpider(scrapy.Spider):
    name = "education"
    start_urls = ['http://edu.qq.com/edunew']


    def parse_single(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//div[@class="qq_article"]/div/h1/text()').extract_first()
        page_info = response.xpath('//div[@class="a_Info"]')
        item['time'] = page_info.xpath('.//span[@class="a_time"]/text()').extract_first().strip()
        item['category'] = "education"
        src = page_info.xpath('.//span[@class="a_source"]/text()').extract_first()
        url = None
        if url is None or src is None:
            item['src'] = "腾讯教育"
        else:
            item['src'] = src
            item['url'] = url
        content = " ".join(response.xpath('//div[@id="Cnt-Main-Article-QQ"]/node()').extract())
        content = content.replace("max-width: 500px", "max-width: 100%")
        if "J_Play" not in content:
            item['content'] = content
        yield item

    def parse(self, response):
        main_part = response.xpath("//div[@class='pageList']")
        second_part = response.xpath("//ul[@class='newsList']")
        page_url = main_part.xpath(".//dt/a/@href").extract() \
                   + second_part.xpath(".//li/a/@href").extract()
        for href in page_url:
            href = response.urljoin(href)
            if not (href.endswith("html") or href.endswith("htm")):
                continue
            item = NewsItem()
            item['url'] = href
            request = scrapy.Request(item['url'], callback=self.parse_single)
            request.meta['item'] = item
            yield request

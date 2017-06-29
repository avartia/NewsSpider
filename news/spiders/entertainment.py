# -*- coding: utf-8 -*-
import scrapy

from news.items import NewsItem


class EntertainmentSpider(scrapy.Spider):
    name = "entertainment"

    start_urls = ['http://news.163.com/special/0001386F/rank_ent.html']


    def parse_single(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//div[@class="post_content_main"]/h1/text()').extract_first()
        page_info = response.xpath('//div[@class="post_time_source"]')
        item['time'] = page_info.xpath('./text()').extract_first()[0:-5].strip()
        item['category'] = "entertainment"
        src = None
        url = None
        if url is None or src is None:
            item['src'] = "网易娱乐"
        else:
            item['src'] = src
            item['url'] = url
        content = " ".join(response.xpath('//div[@id="endText"]/node()').extract())
        content = content.replace("max-width: 500px", "max-width: 100%")
        if "J_Play" not in content:
            item['content'] = content
        yield item

    def parse(self, response):
        main_part = response.xpath("//div[@class='tabContents active']")
        page_url = main_part.xpath(".//a/@href").extract()
        for href in page_url:
            href = response.urljoin(href)
            if not (href.endswith("html") or href.endswith("htm")):
                continue
            item = NewsItem()
            item['url'] = href
            request = scrapy.Request(item['url'], callback=self.parse_single)
            request.meta['item'] = item
            yield request



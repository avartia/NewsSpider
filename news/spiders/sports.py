# -*- coding: utf-8 -*-
import scrapy

from news.items import NewsItem


class SportsSpider(scrapy.Spider):
    name = "sports"
    start_urls = ['https://voice.hupu.com/hot/1', 'https://voice.hupu.com/hot/2', 'https://voice.hupu.com/hot/3',
                  'https://voice.hupu.com/hot/4', 'https://voice.hupu.com/hot/5']
    allowed_domains = ['voice.hupu.com']

    def parse_single(self, response):
        item = response.meta['item']
        item['title'] = response.xpath('//div[@class="voice-main"]/div[@class="artical-title"]/h1/text()').extract_first()
        page_info = response.xpath('//div[@class="artical-info"]')
        item['time'] = page_info.xpath('.//span/a[@class="time"]/span/text()').extract_first().strip()
        item['category'] = "sports"
        src = page_info.xpath('.//span[@class="comeFrom"]/a/text()').extract_first()
        url = page_info.xpath('.//span[@class="comeFrom"]/a/@href').extract_first()
        if url is None or src is None:
            item['src'] = "新浪新闻"
        else:
            item['src'] = src
            item['url'] = url
        content = " ".join(response.xpath('//div[@class="artical-content-read"]/node()').extract())
        content = content.replace("max-width: 660px", "max-width: 100%")
        if "J_Play" not in content:
            item['content'] = content
        yield item

    def parse(self, response):
        main_part = response.xpath("//div[@class='voice-card-list']")
        page_url = main_part.xpath(".//div/div[@class='card-fullText-hd']/a/@href").extract()
        for href in page_url:
            if not (href.startswith("https://"+self.allowed_domains[0]) and (href.endswith("html") or href.endswith("htm"))):
                continue
            item = NewsItem()
            item['url'] = href
            request = scrapy.Request(item['url'], callback=self.parse_single)
            request.meta['item'] = item
            yield request



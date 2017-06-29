# -*- coding: utf-8 -*-
import scrapy

from news.items import NewsItem


class FinanceSpider(scrapy.Spider):
    name = "finance"
    start_urls = ['http://finance.sina.com.cn/']

    def parse_single(self, response):
        try:
            item = response.meta['item']
            item['title'] = response.xpath('//div[@class="page-header"]/h1[@id="artibodyTitle"]/text()').extract_first()
            page_info = response.xpath('//div[@class="page-info"]')
            item['time'] = page_info.xpath('.//span[@class="time-source"]/text()').extract_first().strip()
            item['category'] = "finance"
            src = page_info.xpath('.//span[@class="time-source"]/span/a/text()').extract_first()
            url = page_info.xpath('.//span[@class="time-source"]/span/a/@href').extract_first()
            if url is None or src is None:
                item['src'] = "新浪财经"
            else:
                item['src'] = src
                item['url'] = url
            content = " ".join(response.xpath('//div[@id="artibody"]/node()').extract())
            content = content.replace("max-width: 500px", "max-width: 100%")
            if "J_Play" not in content:
                item['content'] = content
            yield item
        except Exception as e:
            print(e)

    def parse(self, response):
        try:
            main_part = response.xpath("//div[@id='fin_tabs0_c0']")[0]
            second_part = response.xpath("//div[@class='m-p1-m-blk2']")[0]
            third_part = response.xpath("//div[@id='directAd_huaan_04']")[0]
            page_url = main_part.xpath(".//h3[@data-client='headline']/a/@href").extract() \
                       + main_part.xpath(".//p[@data-client='headline']/a/@href").extract() \
                       + main_part.xpath(".//li/a/@href").extract() \
                        + second_part.xpath(".//h3/a/@href").extract() \
                        + second_part.xpath(".//p/a/@href").extract() \
                        + second_part.xpath(".//li/a/@href").extract() \
                       + third_part.xpath(".//h3/a/@href").extract() \
                       + third_part.xpath(".//p/a/@href").extract() \
                       + third_part.xpath(".//li/a/@href").extract()
            for href in page_url:
                if not (href.startswith(self.start_urls[0]) and (href.endswith("html") or href.endswith("htm"))):
                    continue
                print(href)
                item = NewsItem()
                item['url'] = href
                request = scrapy.Request(item['url'], callback=self.parse_single)
                request.meta['item'] = item
                yield request
        except Exception as e:
            print(e)


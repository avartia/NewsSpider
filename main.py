# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/6/20

from scrapy import cmdline
from threading import Timer


def excecute_spider(inc):
    cmdline.execute("scrapy crawl sina-news".split())
    cmdline.execute("scrapy crawl education".split())
    cmdline.execute("scrapy crawl entertainment".split())
    cmdline.execute("scrapy crawl sports".split())
    cmdline.execute("scrapy crawl finance".split())
    cmdline.execute("scrapy crawl science".split())
    t = Timer(inc, excecute_spider, (inc, ))
    t.start()

if __name__ == "__main__":
    # 每隔一个小时调用一次
    excecute_spider(3600)
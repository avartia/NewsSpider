# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/6/20

from scrapy import cmdline

if __name__ == "__main__":
    cmdline.execute("scrapy crawl sina-news".split())
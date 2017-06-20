# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from news.settings import *
import pymysql
from news.items import NewsItem
from scrapy import log
import re

cater_dict = {"main": 0}

class NewsPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=MYSQL_HOST,
            db=MYSQL_DB,
            user=MYSQL_USER,
            passwd=MYSQL_PWD,
            charset='utf8',
            use_unicode=True
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == NewsItem:
            if item['src'] is None or item['url'] is None or item['time'] is None or item['category'] is None or item['title'] is None or item['content'] is None:
                pass
            else:
                try:
                    item['time'] = item['time'].replace('年', '-')
                    item['time'] = item['time'].replace('月', '-')
                    item['time'] = item['time'].replace('日', ' ')
                    item['time'] = item['time'].strip('\t\n')
                    if item['time'].count(':') == 1:
                        item['time'] += ':00'
                    r = re.compile("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
                    if not r.match(item['time']):
                        raise Exception("wrong datetime format!")
                    self.cursor.execute("select * from news where url = %s", (item['url']))
                    ret = self.cursor.fetchone()
                    if ret is None:
                        insert_sql = "insert into news (time, src, url, category, title, content) VALUES ('%s', '%s', '%s', %s, '%s', '%s')"\
                            %(item['time'], item['src'], item['url'], cater_dict.get(item['category'], 0), item['title'],item['content'])
                        self.cursor.execute(insert_sql)
                        self.connect.commit()
                except Exception as error:
                    log.msg(error)
        return item


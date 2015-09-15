# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
from collections import OrderedDict
import json


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('manong-decodeurl.json', 'w', encoding='gbk')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        print line
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()
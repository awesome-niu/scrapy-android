# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
from collections import OrderedDict
import json
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('techandroid.json', 'w', encoding='gbk')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        print line
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_HOST'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DATABASE']]
        self.collection = db[settings['MONGODB_COLLECTION']]




    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!",level=log.DEBUG, spider=spider)
        return item

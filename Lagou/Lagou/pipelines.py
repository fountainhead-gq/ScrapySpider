# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.conf import settings
import pymongo


class LagouPipeline(object):
    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        dbname = settings['MONGODB_DB_NAME']
        collection = settings['MONGODB_COLLECTION']
        connection = pymongo.MongoClient(host, port)
        db = connection[dbname]
        self.collection = db[collection]

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

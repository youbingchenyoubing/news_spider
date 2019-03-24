# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# -*- coding: utf-8 -*-
#coding=utf-8   
from preprocess.different_process import *
import sys 
from scrapy.exceptions import DropItem
sys.path.append('..')
from news_mongodb.db_connection import MongoDBConnection
reload(sys)  
sys.setdefaultencoding('utf8')
try:
    import cPickle as pickle
except:
    import pickle




class PreProcessItem(object): #这个预处理要在存入数据库之前先处理
# 在存储之前，将原始数据处理一下
    def __init__(self,wrong_file):

        self.wrong_file = wrong_file


    def process_item(self,item,spider):

        if item['preprocess_class']  =='':
            #print 'no_deal_class'
            return item
        
        preprocess_object = globals()[item['preprocess_class']]() #针对不同的网站，创建不同预处理的类

        temp_time = item['article_publish_time']

        time_isvalid = preprocess_object.update_publish_time(item) # 格式化时间
        #print item['article_publish_time']
        preprocess_object.update_article_source_from(item) # 格式化文章来源
        
        preprocess_object.update_article_title(item)  #格式化文章标题
        #print item['article_title']
        #print "time=%s,source_from=%s"%(item['article_publish_time'],item['article_source_from'])
        if time_isvalid:

            return item
        else: #2017/04/08 添加的代码
            #print temp_time
            #print("article_publish_time is error in:{},temp_time:{}",{item['article_url']},{temp_time})
            # 写日志
            error_body = "文章日期出错,文章地址:" + item['article_url'] + " 爬虫的时间格式:"+ temp_time + " 处理后的时间为:"+ item['article_publish_time'] + "\n"

            with open(self.wrong_file,'a') as f:

                f.write(error_body)

            raise DropItem("article_publish_time is error in %s",item['article_url'])

    @classmethod
    def from_crawler(cls,crawler):
        return cls(

            wrong_file = crawler.settings.get('WRONG_FILE')
            )

#存入mongoDB数据库
class MongoDBPipline(object):
    def __init__(self,wrong_file):

       self.wrong_file = wrong_file

    
    def open_spider(self,spider):
        #连接数据库
        #print '连接数据库'
        self.mongodb_obj = MongoDBConnection()

        self.collection = self.mongodb_obj.dbConnectionTemp()

    def process_item(self, item, spider):
        
        try:
            row = dict(item)
            del row['preprocess_class']
            self.collection.insert(row)
            #print "插入成功"
        except BaseException,error:
            wrong_body = "写入mongoDB数据库出错:"+str(error)+"\n"
            with open(self.wrong_file,'a') as f:
                f.write(wrong_body)


    def close_spider(self, spider):

        self.mongodb_obj.dbClose() #关闭数据库

    @classmethod
    def from_crawler(cls,crawler):

        return cls(
            wrong_file = crawler.settings.get('WRONG_FILE')
            )
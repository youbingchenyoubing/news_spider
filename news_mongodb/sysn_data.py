#coding=utf-8
import sys
import os
from db_connection import MongoDBConnection
from bson import ObjectId
import re
import logging
import datetime
import time

import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='sysn_data.log',
    filemode='a')

class ArticleDAO(object):
    def __init__(self, label):
        self.mongoDB = MongoDBConnection(label)


root_path = os.path.join(os.path.dirname(__file__),os.pardir,os.pardir)
sys.path.append(root_path)

from news_web.news_web_app.es import ES


def syns_data(startTimeStr):
        # 将数据同步到es中
        try:
            mongoDB = MongoDBConnection("articles_testN") 
            logging.info("[sysn_data] startTimeStr:" + startTimeStr)
            endTime = datetime.datetime.now()
            endTimeStr = endTime.strftime('%Y-%m-%d')
            curTime = datetime.datetime.strptime(startTimeStr, "%Y-%m-%d")

            print "startTime:", curTime
            print "endTime", endTimeStr
            es = ES()
            while curTime <= endTime:
                curTimeStr = curTime.strftime('%Y-%m-%d')
                coll = mongoDB.dbConnection()
                logging.info("[sysn_data] ** time: " +curTimeStr)
                print "******  time:",curTimeStr
                data_list = coll.find({'article_publish_time':curTimeStr}, no_cursor_timeout=True)
                mongoDB.dbClose()
                for one_data in data_list:
                    url = "http://localhost:9200/news_spider_db/articles_testN/" + str(one_data["_id"])
                    print one_data["_id"]
                    one_data.pop("_id") 
                    result = es.put(url, one_data)
                    print result
                curTime = curTime + datetime.timedelta(days = 1)
        except BaseException, e:
            logging.error(e)


syns_data("2006-09-07")

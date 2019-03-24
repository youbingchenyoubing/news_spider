#coding=utf-8

import sys
import datetime
sys.path.append('..')

from news_mongodb.db_operation import MongoDBTempInterface
from news_spider.preprocess.preProcessItem import BasePreProcessItem
from news_spider.preprocess.update_settings import UpdateSettings
from news_spider.time_translation.time_operation import TimeOperate
import setting_for_update







if __name__ == '__main__':

    mongodb_object = MongoDBTempInterface(setting_for_update.update_rate)
    
    #while True:

    data = mongodb_object.testextractPagination(0)

    #for onedata in data:

       # print onedata['_id']

    # dict_time = ['1','2','3']

    # if not '4' in dict_time:
    #     print "hello"

    mongodb_object.batchdelete(data)

    #del update_obj


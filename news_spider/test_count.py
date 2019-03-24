# -*- coding: utf-8 -*-

# 爬虫之前检查中间库是否存在数据，如果存在数据，则有两种情况：
# 1.断电的时候，还在爬数据，所以突然断电的时候，程序还不记录爬虫的位置
# 2.上一次更新还未结束，也就是上次处理的数据还有
# 为了减少数据重复的可能性和数据丢失的可能性，这个程序在爬虫之前要运行
import sys
import os
import time
#import datetime
sys.path.append('..')
sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir))
from news_mongodb.db_operation import MongoDBTempInterface
from news_spider.spiders.Mail_2.myself_email import morePeopleSend

from news_spider.time_translation.time_operation import TimeOperate

def singleton(cls):

    instance = {}

    def wrapper(*args,**kwargs):

        if cls not in instance:

            instance[cls] = cls(*args,**kwargs)

        return instance[cls]
    return wrapper

@singleton
class check(object):
    def __init__(self):

        self.email_time = None
        self.mongo_obj = MongoDBTempInterface()
        self.email_obj = morePeopleSend()
        self.time_obj = TimeOperate()
        self.times = 0
        self.minutes = 60
        self.max_times = 24
    def check_database(self):

        try:
          count  = self.mongo_obj.tempdatacounttemp()
          print "count=",count



        except BaseException,error:

          self.email_obj.send_email("检查程序运行错误","Error:"+ str(error))

          return False
    def __check_time(self,time_now):  #检查上一次发送的邮件发送的时间

        if not self.email_time:

            return True

        if self.time_obj.difftimeminitue(self.email_time,time_now) > self.minutes:

            return True
        else:
            return False
    def break_time(self):

        if self.times > self.max_times:

            self.email_obj.send_email("结束自动爬虫程序的运行","程序已经等待了" + str(self.times)+"小时，但是我们提醒的问题还未得到有效的解决，为了减少机器的负担，我们放弃此次的自动化爬虫")

            return True

        else:

            return False




if __name__ == "__main__":
    check_obj = check()

    #while not check_obj.check_database():
    check_obj.check_database()
        #time.sleep(1800)
        #if check_obj.break_time():
            #exit(1)
    #exit(0)	



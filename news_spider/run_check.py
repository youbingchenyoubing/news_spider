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
          count  = self.mongo_obj.tempdatacount()
          #print "count=",count
          time_now = self.time_obj.getnow()
          if count == 0:
              return True
          elif count != 0 and self.__check_time(time_now):
              content = "数据残留的原因：\n 1.断电造成的爬虫运行到一半就强制结束\n2.断电造成的更新程序运行到一半就强制结束\n 请相关人员进行排查,如果是第一种原因造成的，请手动清理,谢谢合作,第二种原因造成的，请手动启动更新程序，完成所有更新，为了爬虫程序尽快正常运行。谢谢合作！！！"
              self.email_obj.send_email("此次爬虫检查:第"+str(self.times + 1)+ "次邮件通知:"+"数据残留提醒",content)
              self.email_time = time_now
              self.times = self.times + 1
              return False
          elif not count  and self.__check_time(time_now):
              print "count=",count
              self.email_obj.send_email("此次爬虫检查:第"+str(self.times + 1)+ "次邮件通知:"+"统计数据出错","为了爬虫程序尽快正常运行请尽快处理,详细见错误数据库操作日志文件")
              self.email_time = time_now
              self.times = self.times + 1
              return False
          else:
              print "邮件提醒的错误,还未得到处理"
              return False



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


    def __del__(self):
        print "关闭数据库"
        self.mongo_obj.db_close()


if __name__ == "__main__":
    check_obj = check()

    while not check_obj.check_database():
    #check_obj.check_database()
        time.sleep(1800) # 睡眠半个小时，防止对数据库造成压力
        if check_obj.break_time():
            del check_obj
            exit(1)
    del check_obj
    exit(0)	



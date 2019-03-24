
# -*- coding: utf-8 -*-
#coding=utf-8   

#这个文件代码主要重新爬取数据库中一些没爬出内容的文章
import os
import sys
mongo_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
sys.path.append(mongo_path)
from news_mongodb.db_operation_simple import news_operation
from mysetting.json_parse import JsonLoad
from spiders.re_crawler import Spider_Operation
from preprocess.preProcessItem import BasePreProcessItem
from spiders.Mail_2.myself_email import TextEmail
from spiders.Mail_2.myself_email import Email
from time_translation.time_operation import  TimeOperate


class Re_Spider(object):

    def __init__(self,setting_file):

        self.filename = settings_file
        self.json_object = JsonLoad(settings_file)

        self.settings = self.json_object.getdata()
        #print("配置文件:%s" %(self.settings))
        #self.db_operation = news_operation()
        self.db_operation = news_operation(self.settings['record_log'])
        
        self.spider_operation = Spider_Operation(self.settings)

        self.vector_generator = BasePreProcessItem()
       
        self.time_operation = TimeOperate()

    def day_by_day_update(self):

        try:
            if self.settings['start_time'] == "" or self.settings['stop_time'] == "":
                raise Exception("请配置起始时间")
            update_time = self.time_operation.str2date(self.settings['start_time'])

            while str(update_time) >= self.settings['stop_time']:
                
                self.settings['start_time'] = str(update_time)
                print("进度:%s" %(update_time))

                self.settings['extract_condition']['article_publish_time'] = str(update_time)

                self.__spider_for_page()

                self.db_operation.reset_para()

                update_time = self.time_operation.getthepreviousday(update_time)
            return True

        except BaseException,error:
            self.__error_email_info(error)
            return False
        finally:
            self.json_object.changejson(self.filename) #更新开始时间

    def __spider_for_page(self):
        page  = 0
        url_set = set([])
        
        while True:
            print("页数:",page + 1)
            repeate_id = []
            data = self.db_operation.search_news_page(self.settings['extract_condition'],self.settings['re_spider_page'])

            if data == None or data.count(True) == 0:
                break
            for one_data in data:
                #print one_data
                print "url=",one_data['article_url']
                if one_data['article_url'] in url_set:
                    repeate_id.append(one_data['_id'])
                    print "url:%s重复了" %(one_data['article_url'])
                    continue
                url_set.add(one_data['article_url'])
                if not self.spider_operation.spider(one_data): #爬虫提取内容
                    self.__error_email_info(self.__geneator_info(one_data))
                    return 
                
                self.vector_generator.preProcessConent(one_data) #更新内容向量
                
                if not self.db_operation.update_db(one_data):

                    self.__error_email_info(self.__geneator_info(one_data))
                    return

            if not self.db_operation.delete_batch(repeate_id):
                #info = 
                self.__error_email_info(self.__geneator_info(repeate_id))
                return 
            page = page + 1
            data.close()

            #print "集合是:",url_set
            


    def __error_email_info(self,error):

            txt_object = TextEmail()
            txt_object.send_email("重新爬虫错误通知",str(error))
    def __geneator_info(self,data):

        info = ""

        for one_data in data:
            info = info + str(one_data['_id']) + '\n'
        return info
    def endupdate(self):

        attach_object = Email('结束更新通知',self.settings['record_log'])
        attach_object.send_attachemail()
                


                
            

if __name__ == "__main__":


    settings_file = "/home/developMent/news_spider/news_spider/mysetting/re_spider.json"

    re_spider_object = Re_Spider(settings_file)

    result = re_spider_object.day_by_day_update()

    if result:
        
        re_spider_object.endupdate()


    


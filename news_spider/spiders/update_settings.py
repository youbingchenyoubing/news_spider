# -*- coding: utf-8 -*-
#coding=utf-8   
import os
import sys
from scrapy.utils.project import get_project_settings
sys.path.append(os.path.join(os.path.dirname(__file__),os.pardir))
from time_translation.time_operation import TimeOperate
#from news_mongodb.db_connection import MongoDBConnection
reload(sys)  
sys.setdefaultencoding('utf8')


#这个文件是专门根据不同的爬虫网站重新修改爬虫的设置方案

class UpdateSettings(object):


    def updatesettings(self):
        pass

    def touchfile(self,filename):

        if not os.path.exists(filename):
            file_dir = os.path.split(filename)[0]

            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            os.mknod(filename)    
class SinaUpateSettings(UpdateSettings):
    def __init__(self):
        
        self.time_object =  TimeOperate()
        self.settings = get_project_settings()

    def updatesettings(self):
        
        self.settings['COOKIES_ENABLED'] = False

        self.settings['LOG_FILE'] = self.settings['SINA_LOG_FILE'] + str(self.time_object.gettoday())

        self.settings['WRONG_FILE'] = self.settings['WRONG_FILE'] + self.settings['SINA_WRONG_FILE'] + str(self.time_object.gettoday())

        self.settings['DOWNLOAD_DELAY'] = 0.25
        
        self.settings['RANDOMIZE_DOWNLOAD_DELAY'] = True

        self.touchfile(self.settings['LOG_FILE'])

        self.touchfile(self.settings['WRONG_FILE'])

        #self.settings['MONGODB_CONNECTION'] = MongoDBConnection()

        return self.settings
class FengHuangSettings(UpdateSettings):

    def __init__(self):

        self.time_object = TimeOperate()

    def updatesettings(self,settings):
        settings['DOWNLOAD_DELAY'] = 0.25
        
        settings['RANDOMIZE_DOWNLOAD_DELAY'] = True
        settings['RETRY_PRIORITY_ADJUST'] = 2
        settings['DOWNLOAD_TIMEOUT'] = 180 #因为这个网上特殊，一旦停止之后就不会继续爬虫
        settings['DOWNLOADER_MIDDLEWARES']['scrapy.downloadermiddlewares.retry.RetryMiddleware'] = 550
        settings['COOKIES_ENABLED'] = False
        settings['RETRY_HTTP_CODES'] = [500, 503, 504, 400, 403, 404, 408]
        settings['RETRY_TIMES'] = 100
        settings['LOG_FILE'] = settings['GENERAL_LOG_FILE'] + str(self.time_object.gettoday())

        settings['WRONG_FILE'] = settings['WRONG_FILE'] + settings['SPIDER_WRONG_FILE'] + str(self.time_object.gettoday())

        self.touchfile(settings['LOG_FILE'])

        self.touchfile(settings['WRONG_FILE'])


class GeneralUpdateSettings(UpdateSettings):

    def __init__(self):

        self.time_object = TimeOperate()
        #self.settings = get_project_settings()
    def updatesettings(self,settings):
        settings['LOG_FILE'] = settings['GENERAL_LOG_FILE'] + str(self.time_object.gettoday())

        settings['WRONG_FILE'] = settings['WRONG_FILE'] + settings['SPIDER_WRONG_FILE'] + str(self.time_object.gettoday())

        self.touchfile(settings['LOG_FILE'])

        self.touchfile(settings['WRONG_FILE'])

        #return self.settings




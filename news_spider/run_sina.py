
# -*- coding: utf-8 -*-
#coding=utf-8   
import logging
import time
from spiders.Mail.email import Email
from spiders.sinaSpider import SinaNewSpider
from spiders.sinaSpider_old import SinaOldSpider
#from settings import SINA_JSON_FILE
#from settings import SINA_OLD_START_DATE
#from settings import SINA_NEW_START_DATE
from twisted.internet import reactor,defer
from scrapy.crawler import CrawlerRunner
from mysetting.json_parse import JsonLoad
#from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy.exceptions import CloseSpider
from time_translation.time_operation import  TimeOperate
from preprocess.update_settings import SinaUpateSettings
#import initobject.initobject
import os
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

#x = "hello world"
#针对新浪网的爬虫，由于进入新浪网的滚动新闻列表和时间相关。所以单独开来
update_settings_object = SinaUpateSettings()
settings = update_settings_object.updatesettings()
email_object = Email(settings)
#settings['COOKIES_ENABLED'] = False # 新浪网关闭cookie
runner = CrawlerRunner(settings)
'''
def init_single():
    initobject.initobject.InitSimHash(settings['SIMHASH_ID'])'''

@defer.inlineCallbacks
def run_sina():

    try:
    
        #print settings['LOG_FILE']
        read_json_file = JsonLoad(settings['SINA_JSON_FILE'])
        configure_logging(settings) 

        json_data = read_json_file.getdata()
        


        #runner = CrawlerRunner(settings)
        
        begin_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) # 开始时间

        #current_date = time_strftime("%Y-%m-%d",time.localtime()) # 当天日期
        logging.info('爬虫新浪网开始时间:'+begin_time)
        time_operation = TimeOperate()
        if json_data['start_time'] == '':

            yesterday_date = time_operation.getyesterdaydate() #获得昨天的日期
        else:
            yesterday_date = time_operation.str2date(json_data['start_time'])

        temp_begin_spider_date = yesterday_date
        if str(temp_begin_spider_date) == json_data['stop_time']:
            logging.info('爬虫新浪网结束时间:'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
            os._exit(0)
    
        while True:
            
            if str(yesterday_date) <= json_data['stop_time'] or str(yesterday_date) < settings['SINA_OLD_START_DATE']: #结束新浪的爬取
                #print ''
                    break
            #deal_class = ''
            web_config = ''
            if str(yesterday_date) >= settings['SINA_NEW_START_DATE']:
                web_config = json_data['new_version']

                #deal_class = json_data['new_version']
            else:
                web_config = json_data['old_version']
            #day = day+1
            deal_class = web_config['deal_class']
            #settings['PREPROCESS_CLASS'] = web_config['preprocess_class']
            logging.info('开始爬取日期:'+str(yesterday_date))
            print str(yesterday_date)
                #begin_at = begin_at + 1
            yield runner.crawl(globals()[deal_class],website_config = web_config, spider_date = yesterday_date,settings = settings )
            yesterday_date =  time_operation.getthepreviousday(yesterday_date) # 日期推前一天
        reactor.stop()
        
        json_data['stop_time'] = str(temp_begin_spider_date) #更新停止时间
        end_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) #结束时间
        info_spider = ' begin at :'+begin_time+' end at :'+end_time
        logging.info(info_spider)

        sendbody = "time:"+ end_time + "新浪网爬虫结束" +"\n"

        email_object.send_information(sendbody,"新浪网爬虫结束",True)
        os._exit(0)
    except BaseException,error:
        #date = datetime.datetime.now()
        time_object = TimeOperate()
        date = time_object.getnow()
        logging.exception(error)
        sendbody = "time:" + date.strftime("%Y-%m-%d %H:%M:%S") + "error:" + str(error) + "\n"
        #email_object = Email(settings)
        email_object.send_information(sendbody)
        raise CloseSpider('新浪爬虫失败')
        os._exit(1)

    finally:
        read_json_file.changejson(settings['SINA_JSON_FILE'])

if __name__ =='__main__':
    #init_single()
    run_sina()
    reactor.run()




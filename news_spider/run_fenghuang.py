# -*- coding: utf-8 -*-
#coding=utf-8   

import logging
import time
#import mysetting.json_parse
from settings import SPLIT_JSON_FILE
from spiders.newsSpider_Split import  ArticleSpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
# from spiders.XinHuaWanSpider import XinHuaWanSpider   
from mysetting.json_parse import JsonLoad
from scrapy.utils.project import get_project_settings
from preprocess.update_settings import FengHuangSettings
from scrapy.utils.log import configure_logging
from scrapy.exceptions import CloseSpider
from spiders.Mail.email import Email
#import initobject.initobject
#import os
import sys
import os
reload(sys)  
sys.setdefaultencoding('utf8')

if __name__ == '__main__':

    
    try:
        #read_json_file = JsonLoad(SPLIT_JSON_FILE)
        fenghuang_update_object = FengHuangSettings()
        settings = get_project_settings()
        fenghuang_update_object.updatesettings(settings)
        #print settings
        #print settings['REQUEST_DEPTH_MAX']
        email_object = Email(settings)
        configure_logging(settings)
        read_json_file = JsonLoad(settings['SPLIT_JSON_FILE'])
        json_data = read_json_file.getdata()


        runner = CrawlerRunner(settings)
        # 开始爬虫，为了统计爬虫的时间
        begin_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) # 开始时间
        for json_key in json_data:

            website_config = json_data[json_key] # 取出每个网站的配置
            website_url = website_config['url']
            #website_urls  =  website_config[urls] #
            #website_urls = website_config['urls'] # 取每个网站的urls(每一项是地点的url)
            #print website_urls
            #settings['PREPROCESS_CLASS'] = web_config['preprocess_class'
            #logging.info('开始网站爬虫'+json_key+':''-'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
            runner.crawl(ArticleSpider,website_config = website_config,website_url = website_url,website_key = json_key,settings = settings)
            #logging.info('结束网站爬虫'+json_key+':'+url_key+':'+website_urls[url_key]+'-'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
            
        wait = runner.join()

        wait.addBoth(lambda _: reactor.stop())

        #阻塞进程直到爬虫完毕
        reactor.run()
        #end_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        information = "开始爬虫时间:"+ begin_time + "\n爬虫结束时间: "+ end_time + " 凤凰类别数据爬虫完毕"
        email_object.send_information(information,"完成凤凰类别数据爬虫通知",True) 

        os._exit(0)
        #print "通知成功"   
        #end_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) #结束时间
        #info_spider = ' begin at :'+begin_time+' end at :'+end_time
        #logging.info(info_spider)

    except BaseException,error:
        end_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        information = "time: "+ end_time + "错误:" + str(error) + '\n'
        email_object.send_information(information)
        logging.exception(error)
        raise CloseSpider('爬虫识别')
        os._exit(1)

    finally:
        read_json_file.changejson(settings['SPLIT_JSON_FILE'])

        





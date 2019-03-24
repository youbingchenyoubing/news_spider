# -*- coding: utf-8 -*-
#coding=utf-8   



import logging
import time
#import mysetting.json_parse
#from settings import JSON_FILE
from spiders.newsSpider import  ArticleSpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
# from spiders.XinHuaWanSpider import XinHuaWanSpider 	
from mysetting.json_parse import JsonLoad
from scrapy.utils.project import get_project_settings
from preprocess.update_settings import GeneralUpdateSettings
from scrapy.utils.log import configure_logging
from scrapy.exceptions import CloseSpider
from spiders.Mail.email import Email
#import initobject.initobject
#import os
import sys
reload(sys)  
sys.setdefaultencoding('utf8')

if __name__ == '__main__':


    try:
        
        general_update_object = GeneralUpdateSettings()
        settings = get_project_settings()
        general_update_object.updatesettings(settings)
        #print settings
        #print settings['REQUEST_DEPTH_MAX']
        email_object = Email(settings)
        configure_logging(settings)

        read_json_file = JsonLoad(settings['JSON_FILE'])
    	
        json_data = read_json_file.getdata()

       
        runner = CrawlerRunner(settings)
        # 开始爬虫，为了统计爬虫的时间
        begin_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) # 开始时间
        for json_key in json_data:

            website_config = json_data[json_key] # 取出每个网站的配置

            #website_urls  =  website_config[urls] #
            website_urls = website_config['urls'] # 取每个网站的urls(每一项是地点的url)
            #print website_urls
            #settings['PREPROCESS_CLASS'] = web_config['preprocess_class']
            for url_key in website_urls:
                    #print url_key
                    logging.info('开始网站爬虫'+json_key+':'+url_key+':'+website_urls[url_key]+'-'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
                    runner.crawl(ArticleSpider,website_config = website_config,website_url = website_urls[url_key],website_key = json_key, url_key = url_key)
                    logging.info('结束网站爬虫'+json_key+':'+url_key+':'+website_urls[url_key]+'-'+time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()))
            
        wait = runner.join()

        wait.addBoth(lambda _: reactor.stop())

        #阻塞进程直到爬虫完毕
        reactor.run()        
        end_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) #结束时间
        information = "time: " + end_time + "新华社类别新闻爬虫结束" + "\n"
        email_object.send_information(information,"新华社类别新闻爬虫结束通知",True)
        info_spider = ' begin at :' + begin_time +' end at :'+end_time
        logging.info(info_spider)
        exit(0)

    except BaseException,error:
        end_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) #结束时间
        information = "time: " + end_time + str(error) + "\n"
        email_object.send_information(information)
        logging.exception(error)
        raise CloseSpider('爬虫识别')
        exit(1)

    finally:
        read_json_file.changejson(settings['JSON_FILE'])

        





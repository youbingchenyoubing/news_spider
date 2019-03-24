# -*- coding: utf-8 -*-
#coding=utf-8
import scrapy
import re
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from items import NewsSpiderItem
import chardet
import demjson
#from scrapy.mail import MailSender
from getcomment.comment import Comment
#import simplejson
import re
import urllib2
import sys 

sys.path.append('..')

from time_translation.time_operation import TimeOperate
from js_redirect.urllib_js import verify_js_redirect

reload(sys)  
sys.setdefaultencoding('utf8')

# 新版的新浪爬虫
class SinaNewSpider(scrapy.Spider):

    name = "sinanewversion"

    def __init__(self,website_config,spider_date,settings):

        self.current_date = spider_date

        self.website_config = website_config


        self.current_page = 1
        self.start_urls = []
        self.start_urls.append(website_config['main_url'] + 
            website_config['page_url'] + str(self.current_page) +
            website_config['time_url'] + str(spider_date)
            )
        #print self.start_urls[0]
        #self.inform = False
        self.article = 0
        self.settings = settings
        

    def parse(self,response):
        #print "页数:",self.current_page
        print response.url

        encode =  chardet.detect(response.body)['encoding']

        response_body = response.body.decode(encode,'ignore').encode('utf-8')

        response_body = response_body.split('=',1)[1]
        while response_body !='' and response_body[-1] != '}':
            response_body = response_body[:-1]
        #response_body = json.loads(response_body)
        response_body = demjson.decode(response_body)
        for one_list in response_body['list']:

            url = one_list['url']

            # if not re.match(r'^https?:/{2}\w.+$', url):
            #     date = datetime.datetime.now()
            #     information = "time:"+ date.strftime("%Y-%m-%d %H:%M:%S") + " url:" + url +" " +"不合法\n"
            #     filename = self.settings['WRONG_FILE']
            #     with open(file)
            #     return 
            #print url.encode('utf-8')
            self.article = self.article + 1
            # if self.IsPicOrVideo(url,'http://video.sina.com.cn') or self.IsPicOrVideo(url,'http://slide.ent.sina.com.cn'):
            #     article_item = NewsSpiderItem()
            #     article_item['article_title'] = one_list['title'].encode('utf-8')
            #     article_item['article_url'] = url.encode('utf-8')
            #     self.SetNone(article_item)
            #     yield article_item
            #else:
            yield scrapy.Request(url,callback = self.parse_content)
        
        if len(response_body['list']) == 0:
            return
        else:
            self.current_page = self.current_page + 1
            next_page = self.website_config['main_url'] +  self.website_config['page_url'] + str(self.current_page) + self.website_config['time_url'] + str(self.current_date)
            yield scrapy.Request(next_page, callback = self.parse)
        
       
    def parse_content(self,response):


        #print response.status
        try:
        #print response.url
            article_item = NewsSpiderItem()
            
            article_content_config = self.website_config['content_parse']
            article_item['article_source'] = '新浪网'

            article_item['article_publish_time'] = str(self.current_date)
            
            article_item['article_url'] = response.url
            article_item['article_title'] = response.xpath(article_content_config['title_xpath'])
            article_item['article_content'] = response.xpath(article_content_config['content_xpath'])
            if article_item['article_title'] and  article_item['article_content']:
                article_item['article_title'] = article_item['article_title'].extract()[0].encode('utf-8').replace(' ','')
                article_item['article_content'] = article_item['article_content'].extract()[0].encode('utf-8').strip()
                #if re.search(r'<script type="text/javascript">'.encode('utf-8'),article_item['article_content']):
                    #article_item['article_content'] = '这是一个视频或是包含大量脚本'
            else:
                if not article_item['article_title']:
                    raise Exception("Invalid Title")

                if not article_item['article_content']:
                    result = [True]
                    self.__js_verify(response,result)
                    if not result[1]:
                        article_item['article_title'] = article_item['article_title'].extract()[0].encode('utf-8').replace(' ','')
                        article_item['article_content'] = response.xpath('/html').extract()[0].encode('utf-8').strip()
                    else:

                        return 



            article_item['article_source_from'] = response.xpath(article_content_config['source_xpath'])
            if article_item['article_source_from'] :
                article_item['article_source_from'] = article_item['article_source_from'].extract()[0].encode('utf-8').strip()
            else:
                article_item ['article_source_from'] = ''
            article_item['article_discuss'] =  response.xpath(article_content_config['discuss_xpath'])
            if article_item['article_discuss']:
                article_item['article_discuss'] = article_item['article_discuss'].extract()[0].encode('utf-8').strip()
                #article_item['article_discuss_number'] = response.xpath(article_content_config['discuss_number_xpath'])
                #article_item['article_attend_number'] = response.xpath(article_content_config['attend_number_xpath'])
                comment_object = Comment(self.settings,self.content_config)
                comment_object.get_sina_comment_1(article_item)               
            else:
                article_item['article_discuss'] =  response.xpath(article_content_config['discuss_xpath_2'])
                if article_item['article_discuss']:
                    article_item['article_discuss'] = article_item['article_discuss'].extract()[0].encode('utf-8').strip()
                    comment_object = Comment(self.settings,self.website_config)
                    comment_object.get_sina_comment_2(article_item)
                else:
                    article_item['article_discuss'] = []
                    article_item['article_discuss_number'] = 0
                    article_item['article_attend_number'] = 0


            article_item['preprocess_class'] = self.website_config['preprocess_class']
            #print article_item['article_title']
            yield article_item

        except BaseException,error:

            date=datetime.datetime.now()
            sendbody = "time:" + date.strftime("%Y-%m-%d %H:%M:%S") + " url:" + response.url +" " +str(error)+"\n"

            filename = self.settings['WRONG_FILE']

            with open(filename,'a') as f:
                f.write(sendbody)
    def __js_verify(self,text,result):

        real_url_extract_object = verify_js_redirect()

        real_url = real_url_extract_object.verify_location_replace(text)

        if real_url:
        
            yield scrapy.Request(real_url,callback = self.parse_content)

            #return True

        else:
            result[1] = False
    def __js_verify(self,text,type,result):

        real_url_extract_object = verify_js_redirect()

        real_url = real_url_extract_object.verify_location_replace(text)

        if real_url:
            #result[1] = True
            if type == 1:
                yield scrapy.Request(real_url,callback = self.parsehtml)
            else:
                yield scrapy.Request(real_url,callback = self.parse_content)

        else:
            result[1] = False
    def SetNone(self,article_item):

        article_item['article_source'] = '新浪网'

        article_item['article_source_from'] = ''

        article_item['article_content'] ='这是一个视频或是图片'

        article_item['article_publish_time'] = str(self.current_date)

        article_item['article_discuss'] = ''

        article_item['article_discuss_number'] = 0

        article_item['article_attend_number'] = 0

        #article_item['article_read_number'] = 0
    

        article_item['preprocess_class'] = self.website_config['preprocess_class']




# -*- coding: utf-8 -*-
#coding=utf-8
import scrapy
import re
import datetime
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from items import NewsSpiderItem
#from scrapy.mail import MailSender
from getcomment.comment import Comment
import chardet
import demjson
import json
#import simplejson
import re
import urllib2
import sys
sys.path.append('..')

from time_translation.time_operation import TimeOperate
from js_redirect.urllib_js import verify_js_redirect
reload(sys)  
sys.setdefaultencoding('utf8')

#针对新浪网旧版
class SinaOldSpider(CrawlSpider):

    def __init__(self,website_config,spider_date,settings):


        self.current_date = spider_date

        self.website_config = website_config

        self.settings = settings
        self.time_object = TimeOperate()
        self.start_urls = []
        
        self.start_urls.append(website_config['main_url'] + self.time_object.getyear(spider_date) + self.time_object.getmonth(spider_date)
            + self.time_object.getday(spider_date) + website_config['time_url'])
        self.begin_url = (website_config['main_url'] + self.time_object.getyear(spider_date) + self.time_object.getmonth(spider_date)
            + self.time_object.getday(spider_date) + self.website_config['js_file'])
        #print self.begin_url
        self.js = []
        self.html_url = []
        self.article = 0
        #self.inform = False
        self.page_num = 0

    def parse(self,response):
        print response.url
        if self.isnew(response.body):
            #parsejson()  # response的内容是json格式
            for one_url in self.js:
                #print str(oneurl.replace('\"',''))
                yield scrapy.Request(one_url.replace('\"',''), callback = self.parsejson)
        elif str(self.current_date) < self.settings['SINA_MID_START_DATE'] and self.ishtml(response):
            for one_url in self.html_url:
                yield scrapy.Request(one_url, callback = self.parsehtml)

        else:

            entry_js = self.begin_url + str(self.page_num) + self.website_config['js_suffix']

            yield scrapy.Request(entry_js,callback = self.parse_page_js)

    def parse_page_js(self,response):
        #print response.url
        #if response.body == "banned":
            #print "banned by server, begin use proxy"
        encode = chardet.detect(response.body)['encoding']
        #print encode
        response_body = response.body.decode(encode,'ignore').encode('utf-8')
        #re.sub(r'[\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]'.encode('utf-8'),'',response_body)
        response_body = re.search(r'var sinaRss = .*'.encode('utf-8'),response_body)

        if response_body:
            response_body = response_body.group()
            response_body = response_body.split('=',1)[1]
            #response_body = list(response_body)
            #print type(response_body)
            #re.sub(r'=','',response_body)
            #index = response_body.rfind('=')
            #print index
            #response_body[index] = ''
            index = response_body.rfind(';')
            #print response_body
            if index != -1:
                response_body = response_body[:index]
                
                while response_body!="" and response_body[-1] !=']':
                    response_body = response_body[:-1]
                #response_body = eval(response_body) #可以把list,tuple,dict和string相互转化

                try:
                    #print response_body[75224]
                    response_body = json.loads(response_body,strict = False)
                
                    for one_response in response_body:
                        url = one_response[-2]
            
                        if re.match(r'^https?:/{2}\w.+$', url):  
                            yield scrapy.Request(url, callback = self.parsehtml)
                    if len(response_body) <= 0:
                        return
                except BaseException,error:
                    self.__write_log(error)
                
                self.page_num = self.page_num + 1
                next_page_js = self.begin_url + str(self.page_num) + self.website_config['js_suffix']
                yield scrapy.Request(next_page_js,callback = self.parse_page_js)    
        else:
            print "error when search Rss something"
  

    # 如果是json格式的,并且js是在response中提取出来的
    def parsejson(self,response):
        #print "hello"
        #print response.body
        #print response.url
        #print response.url
        encode = chardet.detect(response.body)['encoding']

        response_body = response.body.decode(encode,'ignore').encode('utf-8')
    
        response_body = response_body.split('=',1)[1]

        index  = response_body.rfind('if')

        if index != -1:
            response_body = response_body[:index]
            while response_body!='' and response_body[-1] !='}':
                response_body = response_body[:-1]
        response_body = demjson.decode(response_body)
        #print response_body

        for one_item in response_body['item']:
            url = one_item['link']
            self.article = self.article + 1
            #if self.IsPicOrVideo(url,'http://video.sina.com.cn') or self.IsPicOrVideo(url,'http://slide.ent.sina.com.cn'):
                #article_item = NewsSpiderItem()
                #article_item['article_title'] = one_item['title'].encode('utf-8')
                #article_item['article_url'] = url.encode('utf-8')
                #self.SetNone(article_item)
                #yield article_item       
            
            yield scrapy.Request(url, callback = self.parse_content)
    def parsehtml(self,response):
        #url = response_body.xpath(self.website_config['link'])
        #print response.url
        #print response.status
        try:
            article_content_config = self.website_config['html_content']
            article_item = NewsSpiderItem()
            article_item['article_source'] = '新浪网'

            article_item['article_publish_time'] = str(self.current_date)
            
            article_item['article_url'] = response.url
            article_item['article_title'] = response.xpath(article_content_config['title_xpath'])
            article_item['article_content'] = response.xpath(article_content_config['content_xpath'])
            if article_item['article_title'] and  article_item['article_content']:
                article_item['article_title'] = article_item['article_title'].extract()[0].encode('utf-8').replace(' ','')
                temp_content = article_item['article_content']
                article_item['article_content'] = ''
                for i in xrange(len(temp_content)):

                    article_item['article_content'] = article_item['article_content'] + temp_content.extract()[i].encode('utf-8').strip()
                #if re.search(r'<script type="text/javascript">'.encode('utf-8'),article_item['article_content']):
                    #article_item['article_content'] = '这是一个视频或是包含大量脚本'
            else:
                if not article_item['article_title']:
                    raise Exception("Invalid Title")
                if not article_item['article_content']:
                    result = [True]
                    self.__js_verify(response,1,result)
                    if not result[1]:
                        article_item['article_content'] = response.xpath('/html').extract()[0].encode('utf-8').strip()
                        article_item['article_title'] = article_item['article_title'].extract()[0].encode('utf-8').replace(' ','')
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
                comment_object = Comment(self.settings,self.website_config)
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
            #print '评论:',article_item['article_discuss']
            #print '评论数目:', article_item['article_discuss_number']
            #print '参与人数:', article_item['article_attend_number']
            #article_item['article_read_number']  = 0
            article_item['preprocess_class'] = self.website_config['preprocess_class']
            #print('title:%s,url:%s'%(article_item['article_source_from'],article_item['article_url']))
            yield article_item
        except BaseException,error:

            date=datetime.datetime.now()
            sendbody = "time:" + date.strftime("%Y-%m-%d %H:%M:%S") + " url:" + response.url +" " +str(error)+"\n"
            '''
            if self.inform == False:
                
                mailer = MailSender.from_settings(self.settings)
                mailer.send(to=["840704140@qq.com"], subject="爬虫报错", body = sendbody+"错误写入:" + self.settings['WRONG_FILE'] )
                self.inform = True'''
            filename = self.settings['WRONG_FILE']

            with open(filename,'a') as f:
                f.write(sendbody)
            
    def parse_content(self,response):

        #print response.status
        try:
            article_content_config = self.website_config['content_parse']
            article_item = NewsSpiderItem()
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
                    if not self.__js_verify(response,2):
                        article_item['article_title'] = article_item['article_title'].extract()[0].encode('utf-8').replace(' ','')
                        article_item['article_content'] = response.xpath('/html').extract()[0].encode('utf-8').strip()
                    else:
                        return 

            article_item['article_source_from'] = response.xpath(article_content_config['source_xpath'])
            if article_item['article_source_from'] :
                article_item['article_source_from'] = article_item['article_source_from'] .extract()[0].encode('utf-8').strip()
            else:
                article_item ['article_source_from'] = ''
            article_item['article_discuss'] =  response.xpath(article_content_config['discuss_xpath'])
            if article_item['article_discuss']:
                article_item['article_discuss'] = article_item['article_discuss'].extract()[0].encode('utf-8').strip()
                #article_item['article_discuss_number'] = response.xpath(article_content_config['discuss_number_xpath'])
                #article_item['article_attend_number'] = response.xpath(article_content_config['attend_number_xpath'])
                comment_object = Comment(self.settings,self.website_config)
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
            #print '评论:',article_item['article_discuss']
            #print '评论数目:', article_item['article_discuss_number']
            #print '参与人数:', article_item['article_attend_number']
            #article_item['article_read_number']  = 0
            article_item['preprocess_class'] = self.website_config['preprocess_class']

            yield article_item
        except BaseException,error:

            date=datetime.datetime.now()
            sendbody = "time:" + date.strftime("%Y-%m-%d %H:%M:%S") + " url:" + response.url +" " +str(error)+"\n"
            '''
            if self.inform == False:
                
                mailer = MailSender.from_settings(self.settings)
                mailer.send(to=["840704140@qq.com"], subject="爬虫报错", body = sendbody+"错误写入:" + self.settings['WRONG_FILE'] )
                self.inform = True
                '''
            filename = self.settings['WRONG_FILE']

            with open(filename,'a') as f:
                f.write(sendbody)
 
    def isnew(self,response_body):

        encode = chardet.detect(response_body)['encoding']
        #print response_body
        isjs = re.search(r'\"http://rss.sina.com.cn/rollnews/*.+.js'.encode('utf-8'),response_body.decode(encode,'ignore').encode('utf-8'),re.M)

        if isjs:
            self.js =  isjs.group().split(',')
            return True
        else:
            return False

    def ishtml(self,response):

        url_link = response.xpath(self.website_config['html_path'])

        if url_link:
            url_link = url_link.extract()
            for i in xrange(len(url_link)):
                if re.match(r'http://.*',url_link[i]):
                    pass
                else:
                    #re.sub(ur'\\.\\./'.encode('utf-8'),'',url_link[i].encode('utf-8'))
                    if re.match(r'\.\./',url_link[i]):
                        url_link[i] = url_link[i][3:]
                    url_link[i] = self.website_config['common_url'] + url_link[i]
                #print url_link[i]
            self.html_url = url_link
            return True
        else:
            
            return False

    # 判断是不是重定向
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
    def __write_log(self,error):

        date=datetime.datetime.now()
        sendbody = "time:" + date.strftime("%Y-%m-%d %H:%M:%S") + " url:" + response.url +" " +str(error)+"\n"
        '''
        if self.inform == False:
            
            mailer = MailSender.from_settings(self.settings)
            mailer.send(to=["840704140@qq.com"], subject="爬虫报错", body = sendbody+"错误写入:" + self.settings['WRONG_FILE'] )
            self.inform = True
            '''
        filename = self.settings['WRONG_FILE']

        with open(filename,'a') as f:
            f.write(sendbody)

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





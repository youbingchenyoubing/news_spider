# -*- coding: utf-8 -*-
#coding=utf-8   

import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse
from posixpath import normpath
from items import NewsSpiderItem
from getcomment.comment import Comment
from Mail.email import Email
import chardet
import sys
import datetime
#from Mail.email import Email
reload(sys)

sys.setdefaultencoding('utf8')


#这个是针对凤凰网网站模板实现

class ArticleSpider(CrawlSpider):


    def __init__(self,website_config,website_url,website_key,settings):

        self.website_config = website_config
        self.start_urls = []
        self.website_url = website_url
        self.start_urls.append(self.website_url)

        self.website_key = website_key

        self.current_page = 1

        self.last_url = website_config['last_url']

        self.settings = settings

        #self.m_stop = False
        self.first_url = ''
        #self.days = 0
        #self.papers = 0
        #self.last_page = False
        self.page = 1
        #self.is_first = False
    def parse(self,response):

        #print "papers=",self.papers

        try:
            
            if response.url != self.website_url: #从前一天开始获取

                print "response.url=%s,page=%s"%(response.url,self.page)
                one_page_links = response.xpath(self.website_config['link_xpath'])

                for one_link in one_page_links:
                    
                    url = one_link.extract().encode('utf-8')
                    #self.papers = self.papers + 1
                    if re.match(r'^https?:/{2}\w.+$', url) : #凤凰网有些链接好傻逼，竟然是空的
                        if self.first_url == '':
                            self.first_url = url
                        if url == self.last_url:
                            print "这次%s与上次的url%s相同"%(url,self.last_url)
                            
                            self.update_config()
                            return 

                        yield scrapy.Request(url,callback = self.parse_content)
                    else:
                        date = datetime.datetime.now()
                        information = "time:"+ date.strftime("%Y-%m-%d %H:%M:%S") + " url:" + response.url +" " +"不合法\n"
                        filename = self.settings['WRONG_FILE']
                        self.write_file(filename,information)
                        
                next_page_url = response.xpath(self.website_config['next_path_xpath']) #因为上一页和下一个放在一个xpath里面

                    #print "获取下一页！！！！！"
               
                if next_page_url and (self.page == 1 or len(next_page_url) != 1): #判断最后一页
                        #print "next_page_url",next_page_url
                    self.page = self.page + 1
                    next_url = next_page_url[len(next_page_url)-1].extract().encode('utf-8')
                    #print next_url
                        #print "下一页",next_url
                    #print "页数:",self.page
                    yield scrapy.Request(next_url, callback = self.parse)
                else: #已经没有下一页按钮，从而获得前一天按钮
                    #print len(next_page_url)
                    previous_day = response.xpath(self.website_config['previous_day_xpath'])

                    if previous_day:

                        previous_day_url = previous_day[0].extract().encode('utf-8')
                        #print previous_day_url
                        self.page = 1
                        yield scrapy.Request(previous_day_url,callback = self.parse)
                    else:
                        #print "end scrawl"
                        self.update_config(True,response.url)
                        return 

            else:
                # 获取前一天的按钮
                previous_day = response.xpath(self.website_config['previous_day_xpath'])
                if previous_day:
                    previous_day_url = previous_day[0].extract().encode('utf-8')
                    #print previous_day_url
                    yield scrapy.Request(previous_day_url,callback = self.parse)
                else:
                    #print "end......"
                    self.update_config(True,response.url)

            
            




        except BaseException,error:
            
            date = datetime.datetime.now()
            information = "time:"+ date.strftime("%Y-%m-%d %H:%M:%S") + " url:" + response.url +" " +str(error)+"\n"
            #print information
            #email_object = Email(self.settings)

            #email_object.send_information(information)
            filename = self.settings['WRONG_FILE']
            self.write_file(filename,information)

                

        


    def parse_content(self,response):
        
        try:
            content_config = self.website_config['content']
            article_title = response.xpath(content_config['title_xpath'])
            article_content = response.xpath(content_config['content_xpath'])
            article_publish_time = response.xpath(content_config['publish_time_xpath'])
            if article_title and article_content and article_publish_time:
                article_title = article_title.extract()[0].encode('utf-8').strip()
                article_content = article_content.extract()[0].encode('utf-8').strip()
                article_publish_time = article_publish_time.extract()[0].encode('utf-8').strip()
            elif article_title and article_publish_time:
                article_title = article_title.extract()[0].encode('utf-8').strip()
                article_content = response.xpath('/html').extract()[0].encode('utf-8').strip()
                article_publish_time = article_publish_time.extract()[0].encode('utf-8').strip()
            else:
                errorInfo = 'Invalid '
                if not article_title:
                    errorInfo += "Title "
                if not article_content:
                    errorInfo +="Content "
                if not article_publish_time:
                    errorInfo += "publish time "
                raise Exception(errorInfo)


            article_source_from = response.xpath(content_config['source_xpath'])

            if article_source_from:
                article_source_from = article_source_from.extract()[0].encode('utf-8').strip()

            else:
                article_source_from = ''
            article_item = NewsSpiderItem()
            article_item['article_title'] = article_title
            article_item['article_content'] = article_content
            article_item['article_url'] = response.url
            article_item['article_source'] = self.website_key
            article_item['preprocess_class'] = self.website_config['preprocess_class']
            article_item['article_source_from'] = article_source_from
            article_item['article_publish_time'] = article_publish_time
            # 获得评论
            comment_object = Comment(self.settings,content_config)
            comment_object.get_fenghuangwang_comment(article_item)
            yield article_item


        except BaseException,error:

            date = datetime.datetime.now()
            information = "time:"+ date.strftime("%Y-%m-%d %H:%M:%S") + " url:" + response.url +" " +str(error)+"\n"
            #print information
            #email_object = Email(self.settings)
            #email_object.send_information(information)
            filename = self.settings['WRONG_FILE']
            self.write_file(filename,information)


           




    def write_file(self,filename,information):

        with open(filename,'a') as f:
            f.write(information)


    def update_config(self,inform = False, url = ""):
        if inform:
            date = datetime.datetime.now()
            email_object = Email(self.settings)

            information =  "爬虫结束时间: "+ date.strftime("%Y-%m-%d %H:%M:%S") + "-结束链接:"+ url +"\n凤凰类别数据爬虫完毕原因:后面真的没有数据或爬虫停止"

            email_object.send_information(information,"凤凰类爬虫结束告知")

        if self.first_url != '':

            self.website_config['last_url'] = self.first_url
    

    def closed(self,reason):

        #print "closed:",reason
        date = datetime.datetime.now()

        email_object = Email(self.settings)
        information = "爬虫结束时间: "+ date.strftime("%Y-%m-%d %H:%M:%S") + " 凤凰类别数据爬虫完毕原因:" + str(reason)
        email_object.send_information(information,"完成凤凰类别数据爬虫通知",True) 
        





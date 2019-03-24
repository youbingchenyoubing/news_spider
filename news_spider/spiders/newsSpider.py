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
import chardet
import sys
reload(sys)

sys.setdefaultencoding('utf8')

class ArticleSpider(CrawlSpider):


    name = "newsarticle"

    def __init__(self,website_config,website_url,website_key,url_key):

       
        self.website_config = website_config

        self.website_key = website_key

        self.url_key = url_key

        self.start_urls = []


        self.start_urls.append(website_url)
        #print start_urls

        self.last_url = website_config['last_url'][url_key]  #找到上次爬虫的题目和time

        #self.first_link = '' #为了保存替换
        self.first_link = '' # 暂存这次爬取的第一条标识，一般是url，也有可能是url的唯一标识
        self.current_page = 1 #当前页数
        self.article = 0; #统计一个连接爬取多少文章数
        self.stop = False 
        #self.file_name = 1
        self.first_url = ''
        #self.title_set = set([])
        self.last_response_body = None
        self.total_page = 10000
        #self.inform = False
       

    def parse(self,response): 
        '''拿到start_urls的链接,给内容解析页使用，如果有下一页，则调用本身的parse()'''

        if response is None or response.body == self.last_response_body: #结束递归
            self.update_config()
            return
 
        self.last_response_body = response.body
        page_article_path = response.xpath(self.website_config['link_xpath']) # 取出一页中所有的页面
        for one_article_path in page_article_path:
            url = urljoin(self.website_config['prefix_link'],one_article_path.xpath('@href').extract()[0].encode('utf-8')) #拼接url
            #print url
            url_id = ''
            if self.website_config['last_url_re'] != '': #带cookie的url
                result = re.search(self.website_config['last_url_re'],url)
                if result:
                    url_id = result.group()
                    #print url_id
                else:
                    #print 'no match'
                    self.stop = True
                    break
            else:
                url_id = url
            if url_id == self.last_url:  # 爬到上次的文章
                 self.stop = True
                 break
            if self.article == 0:
                self.first_link = url_id
                self.first_url = response.url
                if self.website_config['totalpage_xpath'] != '':
                    temp_total_page = response.xpath(self.website_config['totalpage_xpath'])
                    if len(temp_total_page) > 0:
                        temp_total_page = temp_total_page.extract()[0]
                        if self.website_config['totalpage_re'] != '':
                            #encode = chardet.detect(self.website_config['totalpage_re'])['encoding']
                            temp_total_page = re.search(self.website_config['totalpage_re'],temp_total_page)
                            self.total_page = int(temp_total_page.group())
            self.article = self.article + 1
            yield scrapy.Request(url,callback = self.parse_content)

        if self.stop or (len(page_article_path) <= 0) or self.total_page <= self.current_page: # 已经是最后一页了
            self.update_config()
            pass
        else:
            
            if self.website_config['nextpage_xpath'] == '': #如果下一页的链接是js生成的

                
                temp_next_url = self.first_url + self.website_config['nextpage_str']+ str(self.current_page+1)
            else:
                temp_next_url = response.xpath(self.website_config['nextpage_xpath']).extract()[0].encode('utf-8')
            if temp_next_url:  #还有下一页
               
                self.current_page = self.current_page + 1
                print '爬取到(页数,文章数):',(str(self.current_page-1),str(self.article))
                next_url = urljoin(self.website_config['prefix_link'],temp_next_url)
                yield scrapy.Request(next_url,callback = self.parse)
            else:
                self.update_config()
        
         

        

        #提取当前页数

    # 解析单页内容
    def parse_content(self,response):

        if response is None:
            return 
        article_item = NewsSpiderItem()
        try:

            article_content_config = self.website_config['content']

            #print article_content_config['publish_time_xpath']
            article_title = response.xpath(article_content_config['title_xpath'])
            article_content = response.xpath(article_content_config['content_xpath'])

            if article_title and article_content:
                article_title = article_title.extract()[0].encode('utf-8').replace(' ','')
                article_content = article_content.extract()[0].encode('utf-8').strip()

            else:
                raise Exception("Invalid Title or Content Path")

            
            if (len(article_title) != 0) and (len(article_content) !=0):  # 我们要的是这两个都必须不为空的文章
                
                article_item['article_publish_time']  = response.xpath(article_content_config['publish_time_xpath'])
                if article_item['article_publish_time']:
                    article_item['article_publish_time'] = article_item['article_publish_time'].extract()[0].encode('utf-8').strip()
                else:
                    article_item['article_publish_time'] = ''
                    return
                article_item['article_source_from'] = response.xpath(article_content_config['source_xpath'])
                if article_item['article_source_from']:
                    article_item['article_source_from'] = article_item['article_source_from'].extract()[0].encode('utf-8').strip()
                else:
                    article_item['article_source_from'] = ''
                article_item['article_url'] = response.url

                article_item['article_source'] = self.website_key

                article_item['article_title'] = article_title

                article_item['article_content'] = article_content

                article_item['preprocess_class'] = self.website_config['preprocess_class']

                #article_item['label'] = '' #目前文章的分类类别是为空的
                if article_content_config['discuss_xpath'] != '':
                    article_item['article_discuss'] = response.xpath(article_content_config['discuss_xpath'])
                    if article_item['article_discuss']:
                        article_item['article_discuss'] = article_item['article_discuss'].extract()[0].encode('utf-8')
                        globals()[article_content_config['deal_discuss']](article_item)
                    else:
                        self.setnone(article_item)
                else:
                    self.setnone(article_item)
                #print "article"
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



    def setnone(self,article_item):

        article_item['article_discuss'] = []
        article_item['article_discuss_number'] = 0
        article_item['article_attend_number'] = 0
    def generate_url(self,url,index): #生成正规的url

        url_temp = urljoin(self.website_config['prefix_link'],url)

        arr = urlparse(url_temp)

        path = normpath(arr[index])

        return urlunparse((arr.scheme,arr.netloc,path,arr.params,arr.query,arr.fragment
            )
            )
    def update_config(self):  #更新配置

        #print '更新.....'
        #print 'self_link=',self.first_link
        if self.first_link !='':
            self.website_config['last_url'][self.url_key] = self.first_link  #更新下次最后读取的文章，作为递归爬虫结束的条件

            

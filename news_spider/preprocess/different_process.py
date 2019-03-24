# -*- coding: utf-8 -*-
#coding=utf-8   

import sys  

import re
import chardet
import logging
import time
reload(sys)  
sys.setdefaultencoding('utf8')


#这个文件主要是用来处理Item内容的格式，针对不同的网站的处理是不一样

#预处理的类
class BasePreProcessItem(object):
    
    def __init__(self):
        pass


    def update_article_title(self,item): #去掉标题中的\t \r \n

        item['article_title'] = item['article_title'].replace('\r','')

        item['article_title'] = item['article_title'].replace('\n','')

        item['article_title'] = item['article_title'].replace('\t','')
        #print('title:%s,url:%s'%(item['article_title'],item['article_url']))

        #print item['article_title']
    def isValidDate(self,item):
        try:
            time.strptime(item['article_publish_time'],'%Y-%m-%d')

            return True
        except BaseException,error:
            #print error
            return False
#
class XinHuaShePreProcessItem(BasePreProcessItem):

    def update_publish_time(self,item): #格式化文章的日期


        temp_publish_time = item['article_publish_time'].split(' ')[0].split('\t')[0]

        temp_publish_time =re.sub(ur"[\u4e00-\u9fa5]",'-'.decode('utf-8'),temp_publish_time.decode('utf-8'))
        #print result_publish_time.encode('utf-8')

        result_publish_time = temp_publish_time[:-1] #去掉最后一个'-'
        #print result_publish_time

        item['article_publish_time'] = result_publish_time
        
        return self.isValidDate(item)

    def update_article_source_from(self,item): #提取来源
        #temp_source_from = item['article_source_from'].split(' ')

        #temp_source_from.replace(' ','')

        #print temp_source_from

        temp_source_from = re.search(ur"[\u6765][\u6e90].*",item['article_source_from'].decode('utf-8'))
            
        if temp_source_from:
            temp_source_from =  temp_source_from.group()

            temp_source_from = temp_source_from.split('：') #是中文的冒号
            item['article_source_from'] = temp_source_from[-1].strip()

        else:
            logging.info('来源预处理出错')
class SinaPreProcessItem(BasePreProcessItem):

    def update_publish_time(self,item):

        return self.isValidDate(item)
        

    def update_article_source_from(self,item):
        pass
        
        
    
class FengHuangWangProcessItem(BasePreProcessItem):

    def update_publish_time(self,item):


        temp_publish_time = item['article_publish_time'].split(' ')[0].split('\t')[0]

        temp_publish_time = temp_publish_time.replace('.','-') #有些时间是包含.

        temp_publish_time =re.sub(ur"[\u4e00-\u9fa5]",'-'.decode('utf-8'),temp_publish_time.decode('utf-8'))
        #print  result_publish_time[-1]

        if temp_publish_time[-1] == '-':
            #result_publish_time =  #去掉最后一个'-'
        #print result_publish_time

            item['article_publish_time'] = temp_publish_time[:-1]
        else:
            item['article_publish_time'] = temp_publish_time
        
        #print "item['article_publish_time'] = ",item['article_publish_time']
        return self.isValidDate(item)

    def update_article_source_from(self,item):
        pass

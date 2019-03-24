# -*- coding: utf-8 -*-
#coding=utf-8
import urllib2
import random

import sys
import chardet
# import sys
# import os
# # log_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir))
# # sys.path.append(log_path)
# # print sys.path
from error_log.record_error import write_record
from mysetting.json_parse import JsonLoad
from lxml import etree
from scrapy import Selector
from js_redirect.urllib_js import verify_js_redirect


class Spider_Operation(object):

    def __init__(self,settings):
        #print settings
        self.settings = settings
        self.log_obj = write_record(self.settings['record_log']) #写日志对象
        json_object = JsonLoad(self.settings['user_agent_file'])
        self.agent_list =  json_object.getlist()
        self.timeout = self.settings['timeout']
    def spider(self,data):

        try:
            data['article_content'] = None
            #data['flag'] = 'article_content'
            #data['is_video'] = True
            # data['flag'] = 1
            # data['video_info'] =  None
            one_user_agent = random.choice(self.agent_list)
            headers = { 'User-Agent' : one_user_agent }
            request = urllib2.Request(data['article_url'],headers = headers)
            strcontent =  urllib2.urlopen(request,timeout = self.timeout).read()
            if not strcontent:
                raise Exception("爬虫超时")
            #下面三行解决了爬虫乱码的问题
            typeEncode = sys.getfilesystemencoding()##系统默认编码 
            infoencode = chardet.detect(strcontent).get('encoding','utf-8')##通过第3方模块来自动提取网页的编码 
            content = strcontent.decode(infoencode,'ignore').encode(typeEncode)##先转换成unicode编码，然后转换系统编码输出  
            content = Selector(text=content,type="html")

            

            #response_body = response.body.decode(encode,'ignore').encode('utf-8')
            article_content = content.xpath(self.settings['content_xpath'])

            if article_content:

                data['article_content'] = article_content.extract()[0]

            else:
                if not self.__js_verify(strcontent,data):
                    data['article_content'] =  content.xpath(self.settings['body_xpath']).extract()[0]
            return True
        except BaseException,error:

            self.log_obj.write_log("爬虫出错:url:"+ data['article_url'] +"----"+str(error))
            return False
    #判断这个网页是否是js重定向
    def __js__verify(text,data):

        real_url_extract_object = verify_js_redirect()

        real_url = real_url_extract_object.verify_location_replace(text)

        if real_url:
            data['article_url'] = real_url
            return self.spider(data)

        return False








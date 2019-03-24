# -*- coding: utf-8 -*-
#coding=utf-8

import urllib2
import random
import sys
import datetime
#sys.path.append('../../')
from mysetting.json_parse import JsonLoad
class Comment(object):

    def __init__(self,settings = None,website_config = None):

        self.settings = settings
        self.website_config = website_config
    def get_sina_comment_1(self,article_item):
  
        article_item['article_discuss'] = article_item['article_discuss'].split(':')
        article_item['article_discuss_number'] = 0
        article_item['article_attend_number'] = 0
        if len(article_item['article_discuss']) != 2:
            article_item['article_discuss'] = []
            return
        comment_page = 1
        channerl_id = article_item['article_discuss'][0]
        comment_id = article_item['article_discuss'][1]
        # 存储评论
        
        cmntlist = []
        article_item['article_discuss'] = []
        #print 'hello wrold'
        json_object = JsonLoad(self.settings['USER_AGENT_FILE'])
        agent_list =  json_object.getlist()
        while comment_page == 1 or cmntlist != []:
            one_user_agent = random.choice(agent_list)
            headers = { 'User-Agent' : one_user_agent }  
            comment_url = self.website_config['comment_url'] + "&newsid=" + comment_id + "&channel=" + channerl_id + "&page=" + str(comment_page) 
            try:
                request = urllib2.Request(comment_url,headers = headers)
                comment_content =  urllib2.urlopen(request,timeout = self.settings['DOWNLOAD_TIMEOUT']).read()
                if comment_content is None:
                    break
                find_str = "={"

                extract_contain = comment_content[comment_content.index(find_str) + len(find_str) -1:]

                extract_contain = extract_contain.replace('null','None')

                real_content = eval(extract_contain)

                if 'cmntlist' in real_content['result']:
                    cmntlist = real_content['result']['cmntlist']
                else:
                    cmntlist = []
                if cmntlist != []:
                    article_item['article_discuss'].append(cmntlist)
                if comment_page  == 1 and ('count' in real_content['result']):
                    article_item['article_discuss_number'] = int(real_content['result']['count']['show'])
                    article_item['article_attend_number'] = int(real_content['result']['count']['total'])
                comment_page = comment_page + 1
            except BaseException,error:
                date=datetime.datetime.now()
                sendbody = "time:" + date.strftime("%Y-%m-%d %H:%M:%S") + " comment_url:" + comment_url +" " +str(error)+"\n"
                filename = self.settings['WRONG_FILE']

                with open(filename,'a') as f:
                    f.write(sendbody)
                break

    def get_sina_comment_2(self,article_item):
        refer = article_item['article_url']
        article_item['article_discuss'] = article_item['article_discuss'].split('?')
        article_item['article_discuss_number'] = 0
        article_item['article_attend_number'] = 0
        if len(article_item['article_discuss']) != 2:
            article_item['article_discuss'] = []
            return
        comment_page = 1
        lefturl = article_item['article_discuss'][1]
        # 存储评论
        
        cmntlist = []
        article_item['article_discuss'] = []
        #print 'hello wrold'
        json_object = JsonLoad(self.settings['USER_AGENT_FILE'])
        agent_list =  json_object.getlist()
        while comment_page == 1 or cmntlist != []:
            one_user_agent = random.choice(agent_list)
            headers = { 'User-Agent' : one_user_agent,'Referer':refer}  
            comment_url = self.website_config['comment_url'] +'&' +lefturl + "&page=" + str(comment_page) 
            try:
                #print comment_url
                request = urllib2.Request(comment_url,headers = headers)
                comment_content =  urllib2.urlopen(request,timeout = self.settings['DOWNLOAD_TIMEOUT']).read()
                if comment_content is None:
                    break
                find_str = "={"

                extract_contain = comment_content[comment_content.index(find_str) + len(find_str) -1:]

                extract_contain = extract_contain.replace('null','None')

                real_content = eval(extract_contain)

                if 'cmntlist' in real_content['result']:
                    cmntlist = real_content['result']['cmntlist']
                else:
                    cmntlist = []
                if cmntlist != []:
                    article_item['article_discuss'].append(cmntlist)
                if comment_page  == 1 and ('count' in real_content['result']):
                    #print real_content
                    article_item['article_discuss_number'] = int(real_content['result']['count']['show'])
                    article_item['article_attend_number'] = int(real_content['result']['count']['total'])
                comment_page = comment_page + 1
            except BaseException,error:
                date=datetime.datetime.now()
                sendbody = "time:" + date.strftime("%Y-%m-%d %H:%M:%S") + " comment_url:" + comment_url +" " +str(error)+"\n"
                filename = self.settings['WRONG_FILE']

                with open(filename,'a') as f:
                    f.write(sendbody)
                break        
    def get_fenghuangwang_comment(self,article_item):

        comment_url = self.website_config['discuss_url'] + article_item['article_url']

        json_object = JsonLoad(self.settings['USER_AGENT_FILE'])

        agent_list =  json_object.getlist()

        one_user_agent = random.choice(agent_list)
        headers = { 'User-Agent' : one_user_agent,'Referer':article_item['article_url']}
        article_item['article_discuss'] = []
        article_item['article_discuss_number'] = 0
        article_item['article_attend_number'] = 0

        try:

            request = urllib2.Request(comment_url,headers = headers)
            comment_content =  urllib2.urlopen(request,timeout = self.settings['DOWNLOAD_TIMEOUT']).read()

            if not comment_content:

                raise Exception("获取评论出错")
            
            find_str = "={"
            extract_contain = comment_content[comment_content.index(find_str) + len(find_str) -1:]
            #real_content = eval(extract_contain)
            extract_contain = extract_contain.replace('null','None')
            extract_contain = extract_contain.replace('false','None')
            #print len(extract_contain)
            real_content = extract_contain[0:len(extract_contain)-1] #去掉";"
            real_content = eval(real_content) #转化成字典
            #print real_content['count']
            article_item['article_discuss'] = real_content['comments']
            article_item['article_discuss_number'] = int(real_content['count'])
            article_item['article_attend_number'] = int(real_content['join_count'])

        except Exception,error:
            date=datetime.datetime.now()
            sendbody = "time:" + date.strftime("%Y-%m-%d %H:%M:%S") + " comment_url:" + comment_url +" " +str(error)+"\n"
            filename = self.settings['WRONG_FILE']

            with open(filename,'a') as f:
                f.write(sendbody)












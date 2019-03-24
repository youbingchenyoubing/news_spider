#coding=utf-8
import urllib 
import urllib2 
import json
import logging
import sys
import re

type = sys.getfilesystemencoding()

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='news_web.log',
    filemode='a')

class ES(object):
    def __init__(self):
        self.IP = "localhost"
        self.PORT = "9200"
        pass

    def article_search_list(self, search_condition, key=None, DB="articles_testP"):
    	# 来源网站
    	article_source = search_condition['article_source']
        # 是否重复
        article_db = search_condition['article_db']
        # 标注状态
        article_label_state = search_condition['article_label_state']
        # 开始时间
        startTime = search_condition['startTime']
        # 结束时间
        endTime = search_condition['endTime']
        # 当前页
        current_page = search_condition['current_page']
        # 每页显示的页数
        page_size = search_condition['page_size']
        
        query_filter = [
            { "term": { "article_label_state":article_label_state}},
            {"range" : 
                {
                 "article_publish_time" :  # 发布时间
                    {
                        "gte" :startTime,
                        "lte" :endTime
                    }
                }
            }
        ]

        if article_db == 1:
            query_filter.append({ "term":{ "is_repeate":"0"}});

        should_query = []
        if len(article_source) != 0:
            for source in article_source:
                should_query.append({ "match":{"article_source":source}});


        bool_query = {"filter":query_filter}
        if len(should_query) != 0:
            bool_query["should"] = should_query
        
       
        # 关键词
        #if key != None:
        #    search_key = key.split("NOT")
            # 必须包含的关键词
        #    bool_query["must"] = {
        #    "bool":{"should":[{"match": { "article_title": key}},
        #       {"match": { "article_content": key}}]}}

        mutli_query ={
          "query": { 
            "bool": bool_query
          }
          #"sort": { "article_publish_time": { "order": "asc" }} 
        }
        #print "----------"
        #print mutli_query
        #print "---------------"

        sizefrom  = int(page_size) * int(current_page)
        url = "http://" + self.IP + ":" + self.PORT + "/news_spider_db/" \
           + DB + "/_search?size=" + str(page_size)+ "&from=" +str(sizefrom)
        result = es.get(url, mutli_query)
        
        article_list = []
        for line in result:
            article = line["_source"]
            article['article_content'] = self._remove_htmlTags(article['article_content'])
            article['article_content'] = article['article_content'][0: 240]
            article_list.append(article)
            #print line["_source"]
        return article_list

    def _remove_htmlTags(self, html):
        # tag
        tag_re = re.compile(r'<[^>]+>',re.S)
        result = tag_re.sub('', html)

        ## space 
        space_re = re.compile(r'&[^>]+;', re.S)
        result = space_re.sub('', result)
        return result
    

    def get(self, url, values):
        try:
            # 对数据进行JSON格式化编码
	    jdata = json.dumps(values) 
	    # 生成页面请求的完整数据
            req = urllib2.Request(url, jdata)
            # 发送页面请求 
            response = urllib2.urlopen(req) 
            # 获取服务器返回的页面信息
            the_page = response.read()
            result = json.loads(the_page)
            return  result['hits']['hits']
        except BaseException, e:
            logging.error(e) 
            return None          



es = ES()
#print es.get("http://localhost:9200/news_spider_db/articles_testP/_search",{"query":{"match":{"simhash":"1855271740191983003"}}})

search_condition={"startTime":"1999-01-03","endTime":"2018-01-03","page_size":"5",\
 "current_page":"0", "is_repeate":"1", "article_label_state":"1","article_source":["新浪网","凤凰网"]}
#es.article_search_list(search_condition,"两名北约驻阿富汗士兵遇袭身亡")

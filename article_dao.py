# coding=utf-8
from db_connection import MongoDBConnection
from bson import ObjectId
import re
import logging

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='news_web.log',
    filemode='a')

class ArticleDAO(object):
    def __init__(self, label):
        self.mongoDB = MongoDBConnection(label)
    
    
    def article_search_list(self, search_condition):
        try:
            article_source = search_condition['article_source']
            article_db = search_condition['article_db']
            article_label_state = search_condition['article_label_state']
            startTime = search_condition['startTime']
            endTime = search_condition['endTime']
            current_page = search_condition['current_page']
            page_size = search_condition['page_size']
            coll = self.mongoDB.dbConnection()

            condition = {"article_label_state": article_label_state,
                 'article_publish_time':{'$gte': startTime, '$lte':endTime}}
            if len(article_source) != 0: 
                # 如果列表长度为0则查询所有网站新闻
                condition['article_source'] = {'$in': article_source} 
            
            if article_db == 1:
                condition['is_repeate'] = 0
        
            result = coll.find(condition).skip(page_size * current_page).limit(page_size)
            self.mongoDB.dbClose()
            
            article_list = []
            for article in result:
                article['_id'] = str(article['_id'])
                article['id'] = article['_id']
                article['article_content'] = self._remove_htmlTags(article['article_content'])
                article['article_content'] = article['article_content'][0: 240]
                article_list.append(article)
            
            return article_list
        except BaseException, e:
            logging.error(e)
            return None

    def _remove_htmlTags(self, html):
        # tag
        tag_re = re.compile(r'<[^>]+>',re.S)
        result = tag_re.sub('', html)

        ## space 
        space_re = re.compile(r'&[^>]+;', re.S)
        result = space_re.sub('', result)
        return result
     
    def show_article(self, article_id):
        try:
            coll = self.mongoDB.dbConnection()
            result = coll.find_one({"_id":ObjectId(article_id)}) 
            self.mongoDB.dbClose()
            if result:
                result['_id'] = str(result['_id'])
                result['id'] = result['_id']
            return result
        except BaseException, e :
            logging.error(e)
            return None

    def del_article(self, article_id):
        try:
            coll = self.mongoDB.dbConnection()
            result = coll.remove({"_id":ObjectId(article_id)}) 
            self.mongoDB.dbClose()
            return True
        except BaseException, e : 
            logging.error(e)
            return False

    def add_article(self, info):
        try:
            coll = self.mongoDB.dbConnection()
            result = coll.insert(info)
            self.mongoDB.dbClose()
            return result
        except BaseException, e : 
            logging.error(e)
            return None

    def update_article(self, article_id, info):
        try:
            coll = self.mongoDB.dbConnection()
            result = coll.update({"_id":ObjectId(article_id)},{"$set":info})
            self.mongoDB.dbClose()
            return result
        except BaseException, e : 
            logging.error(e)
            return None
        

    def addTag(self, article_id, tag):
        try:
            coll = self.mongoDB.dbConnection()
            result = coll.find_one({"_id":ObjectId(article_id)})
            self.mongoDB.dbClose()
            if result.has_key('tags'):
                tags = result['tags']
                tagList = tags.split(",")
                if tag in tagList:
                    return False
                else:
                    tags = tags + "," + tag
            else:
                tags = tag

            coll = self.mongoDB.dbConnection()
            coll.update({"_id":ObjectId(article_id)}, {"$set":{"tags":tags}})
            self.mongoDB.dbClose()
            return True
        except BaseException, e:
            logging.error(e)
            return False

    def removeTag(self, article_id, tag):
        try:
            coll = self.mongoDB.dbConnection()
            result = coll.find_one({"_id":ObjectId(article_id)})
            self.mongoDB.dbClose()
            if result.has_key('tags'):
                tags = result['tags']
                tagList = tags.split(",")
                tagList.remove(tag)
                if len(tagList) == 0:
                    tags = ""
                else:
                    tags = ",".join(list(tagList))

            else:
                tags = tag

            coll = self.mongoDB.dbConnection()
            coll.update({"_id":ObjectId(article_id)}, {"$set":{"tags":tags}})
            self.mongoDB.dbClose()
            return True
        except BaseException, e:
            logging.error(e)
            return False

    

def test():
    dao = ArticleDAO('articles_test') 
    condition = {"article_source":['新浪网'], "article_db":"0", "article_label_state":0, "startTime":'2017-01-11',
         "endTime":'2017-01-15', "current_page":0, "page_size":20 }
    #result = dao.article_search_list(condition)
    #print result
 
    #print dao.show_article('58794f6fe13823778c72d640')
test()   

# coding=utf-8
from db_connection import MongoDBConnection
from bson import ObjectId
import re
import logging
import datetime
import time
import traceback

logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename='news_mongodb.log',
    filemode='a')

class ArticleDAO(object):
    def __init__(self, label):
        self.mongoDB = MongoDBConnection(label)


    def article_search_list(self, search_condition):
        try:
            logging.info("article_search_list()")
            article_source = search_condition['article_source']
            article_db = search_condition['article_db']
            article_label_state = search_condition['article_label_state']
            startTime = search_condition['startTime']
            endTime = search_condition['endTime']
            current_page = search_condition['current_page']
            page_size = search_condition['page_size']
            article_label = search_condition['article_label']
            timerange_check = search_condition["timerange_check"]
            search_type = search_condition["search_type"]
            tags = search_condition["tags"]

            coll = self.mongoDB.dbConnection()
            condition = {}
            if search_type == "filter_search":
                if timerange_check == 1:
                    condition['article_publish_time'] = {'$gte': startTime, '$lte':endTime}

                if len(article_label_state) != 0:
                    condition['article_label_state'] = {'$in': article_label_state}

                if len(article_label) != 0:
                    condition["article_label"] = {'$in': article_label}

                if len(article_source) != 0:
                    # 如果列表长度为0则查询所有网站新闻
                    condition['article_source'] = {'$in': article_source}
                if len(tags) != 0:
                    orlist = []
                    for tag in tags:
                        orlist.append({"tags":tag.strip()})
                    condition['$or'] = orlist

                if article_db == 1:
                    condition['is_repeate'] = 0

                if search_condition.has_key("update_student"):
                    condition['update_student']= search_condition['update_student']

            print "mongodb condition:", condition
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
            print e
            print traceback.print_exc()
            logging.error(e)
            return []

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

            result["tags"] = tags
            coll = self.mongoDB.dbConnection()
            coll.update({"_id":ObjectId(article_id)}, {"$set":{"tags":tags}})
            self.mongoDB.dbClose()
            return True, {"tags":tags}
        except BaseException, e:
            logging.error(e)
            print e
            print traceback.print_exc()
            return False, {}

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

            result["tags"] = tags
            coll = self.mongoDB.dbConnection()
            coll.update({"_id":ObjectId(article_id)}, {"$set":{"tags":tags}})
            self.mongoDB.dbClose()
            return True, {"tags":tags}
        except BaseException, e:
            logging.error(e)
            return False, {}


    def get_all(self):
        try:
            coll = self.mongoDB.dbConnection()
            result = coll.find()
            self.mongoDB.dbClose()
            article_list = []
            urlSet = set('')
            for article in result:
                if article['article_url'] in urlSet:
                    continue
                article.pop('_id')
                urlSet.add(article['article_url'])
                article_list.append(article)
            return article_list
        except BaseException, e:
            logging.error(e)
            return None

    def add_batch(self, article_list):
        try:
            coll = self.mongoDB.dbConnection()
            count = 0
            print len(article_list)
            for article in article_list:
                count = count + 1
                print count
                result = coll.insert(article)
                print result
            self.mongoDB.dbClose()
            return True
        except BaseException, e:
            logging.error(e)
            return False


    def syns_data(self, syns_tag, startTimeStr):
        # 将数据同步到es中
        try:
            logging.info("[sysn_data] startTimeStr:" + startTimeStr + "  syns_tag:" + str(syns_tag))
            endTime = datetime.datetime.now()
            endTimeStr = endTime.strftime('%Y-%m-%d')
            curTime = datetime.datetime.strptime(startTimeStr, "%Y-%m-%d")

            print "startTime:", curTime
            print "endTime", endTimeStr

            while curTime <= endTime:
                curTimeStr = curTime.strftime('%Y-%m-%d')
                coll = self.mongoDB.dbConnection()
                logging.info("[sysn_data] time: " +curTimeStr)
                print "time:",curTimeStr
                result = coll.update_many({'article_publish_time':curTimeStr},{"$set":{"sysn_switch":syns_tag}})
                print "result.modified_count:", result.modified_count
                self.mongoDB.dbClose()
                curTime = curTime + datetime.timedelta(days = 1)
        except BaseException, e:
            logging.error(e)


def trans_data():
    pdao = ArticleDAO('articles_testP')
    article_list = pdao.get_all()
    print len(article_list)
    nDao = ArticleDAO('articles_testN')
    result = nDao.add_batch(article_list)
    print result



def test():
    dao = ArticleDAO('articles_testN')
    condition = {"article_source":['新浪网'], "article_db":"0", "article_label_state":0, "startTime":'2017-01-11',
         "endTime":'2017-01-15', "current_page":0, "page_size":20 }

    #dao.syns_data(1, "2006-09-06")
    #result = dao.article_search_list(condition)
    #print result

    #print dao.show_article('58794f6fe13823778c72d640')
test()
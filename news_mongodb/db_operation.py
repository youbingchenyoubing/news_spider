#coding=utf-8
import pymongo
import datetime
import db_settings
import os     
import sys
sys.path.append(os.path.dirname(__file__))
from db_connection import MongoDBConnection
#数据库操作 用这份代码，一定记得手动调用 db_close()函数，手动关闭

from news_spider.time_translation.time_operation import TimeOperate
'''
class ArticleInterface(object):

    def __init__(self):

        pass
    def db_close(self):
        pass'''
'''
class ArticleDAO(ArticleInterface):

    def __init__(self):

        self.obj = MongoDBConnection()
        self.collection = self.obj.dbConnection()
    def db_close(self):

        self.obj.dbClose()
    #分页显示
    def article_search_list(self,condition):
        try:
            print "您好，使用者这里查询还没考虑优化"
        article
        except BaseException,error:
            return dict([])

        pass
    def __parseCondition(self,condition):
        for key in condition
        return condition'''

class TempArticleInterface(object):

    def __init__(self):
        pass
    def db_close(self):
        pass
class MongoDBTempInterface(TempArticleInterface):

    def __init__(self,page_list = 100):

        self.obj = MongoDBConnection()
        self.temp_collection = self.obj.dbConnectionTemp()
        self.collection_postive = self.obj.dbConnection()
        self.collection_negative = self.obj.dbConnectionNegative()
        #self.last_objectid = None
        self.page_list = page_list
        self.stop = False
        self.dict_time = {}
        self.loop = 2
        self.filename = db_settings.MONGO_LOG_FILE + str(datetime.date.today())

    def extractPagination(self,pagenumber):
    
        try:
            
            if self.stop:
                return None
            data = self.temp_collection.find({},no_cursor_timeout=True).hint([("article_publish_time",pymongo.ASCENDING)]).skip(pagenumber*self.page_list).limit(self.page_list)
            
            if data.count(True) < self.page_list:
                self.stop = True
            return data
        except BaseException,error:
            self.writeerrorlog(error)
            return None
    def testextractPagination(self,pagenumber): #测试代码
        try:
            if self.stop:
                return None
            data = self.temp_collection.find({"article_source":"凤凰网"},{},no_cursor_timeout=True).hint([("article_publish_time",pymongo.ASCENDING)]).skip(pagenumber*self.page_list).limit(self.page_list)
            
            if data.count(True) < self.page_list:
                self.stop = True
            return data
        except BaseException,error:
            print "错误:{}",{error}
            self.writeerrorlog(error)
            return None

    def db_close(self):

        self.obj.dbClose()

    def _extractPostive(self,date):
        try:
            strdate = str(date)
            data = self.collection_postive.find({"article_publish_time":strdate},{"simhash":1,"_id":0},no_cursor_timeout=True).hint([("article_publish_time",pymongo.ASCENDING)])
            #timeobj = TimeOperate()
            #date = timeobj.str2date(strdate)
            for onedata in data:
                if not self.dict_time.has_key(date):
                    self.dict_time[date] = []

                self.dict_time[date].append(onedata['simhash'])
            data.close() #一定要关闭游标，因为设置这个no_cursor_timeout=True
            #return True
        except BaseException,error:
            self.writeerrorlog(error)
            #return False
        
    def _extractNegative(self,date):

        try:
            strdate = str(date)
            data = self.collection_negative.find({"article_publish_time":strdate},{"simhash":1,"_id":0},no_cursor_timeout=True).hint([("article_publish_time",pymongo.ASCENDING)])

            for onedata in data:
                if not self.dict_time.has_key(date):
                    self.dict_time[date] = []
                self.dict_time[date].append(onedata['simhash'])
            data.close() #一定要关闭游标，因为设置这个no_cursor_timeout=True参数
            #return True
        except BaseException,error:
            self.writeerrorlog(error)
            #return False
    #正式使用的代码
    def getdicttime(self,mindate):

        timeobj = TimeOperate()

        for i in xrange(self.loop):


            #self._extractPostive(mindate) #2017年5月12日开始抛弃正例库

            self._extractNegative(mindate)

            mindate = timeobj.getthepreviousday(mindate)  #获得前一天的时间

        return self.dict_time
    # 爬虫的时候是从前往后爬，所以以前的数据不在数据库
    def getdicttime2(self,mindate):

        timeobj = TimeOperate()

        for i in xrange(self.loop):


            #self._extractPostive(mindate) #2017年5月12日开始抛弃正例库

            self._extractNegative(mindate)

            mindate = timeobj.getthefutureday(mindate) #获得未来一天的时间

        return self.dict_time


    def batchdelete(self,data):

        try:
           
            for onedata in data:
                #print "删除{}",{onedata['_id']}
                self.temp_collection.remove({"_id": onedata['_id']})
            return True

        except BaseException,error:
            self.writeerrorlog(error)
            return False


    def batchinsertnegative(self,negative):


        try:
             if negative:
                 self.collection_negative.insert_many(negative)
             return True
        except BaseException,error:
            self.writeerrorlog(error)
            return False
    
    def batchinsertpositive(self,postive):

        try:
            if postive:
                self.collection_postive.insert_many(postive)
            return True
        except BaseException,error:
            self.writeerrorlog(error)
            return False
    def removedata(self):
        try:
            self.temp_collection.delete_many({})
        except BaseException,error:
            self.writeerrorlog(error)
    def testremove(self):
        try:
            self.collection_negative.delete_many({})
        except BaseException,error:
            self.writeerrorlog(error)
    def writeerrorlog(self,error):
        self.touchfile()
        body = str(datetime.datetime.now()) + ':' +str(error) + '\n'
        with open(self.filename,'a') as f:
            f.write(body)


    def touchfile(self):
        
        if not os.path.exists(self.filename):
            file_dir = os.path.split(self.filename)[0]

            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            os.mknod(self.filename)
    def tempdatacount(self):

        try:
            count = self.temp_collection.count()
            return count
        except BaseException,error:
            self.writeerrorlog(error)
            return None 
    def tempdatacounttemp(self):

        try:
            self.temp_collection = self.obj.dbConnectionTemp()
            count = self.temp_collection.count()
            data = self.temp_collection.find()
            #return data.count(True)
            i = 1
            for one_data in data:
                print i
                i = i + 1
                #print str(one_data['_id'])
            data.close()
            return count
            #return count
        except BaseException,error:
            self.writeerrorlog(error)
            return None
        finally:
            self.temp_collection = self.obj.dbClose()

 
            
 



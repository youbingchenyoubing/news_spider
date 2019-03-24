#coding=utf-8

import os
#from scrapy.utils.project import get_project_settings
import sys
sys.path.append('..')
from news_spider.mysetting.json_parse import JsonLoad
import pymongo


#数据库连接
class DBConnection(object):

    def dbConnection(self):

        pass
    def dbConnectionTemp(self):
        pass

    def __new__(cls,*args,**kwargs):

        if not hasattr(cls,'_instance'):
            cls._instance = super(DBConnection,cls).__new__(cls,*args,**kwargs)
        return cls._instance

class MongoDBConnection(DBConnection):

    def __init__(self,collection_name = None):
        
        #print"初始化"
        #self.settings = get_project_settings()
        self.connection = None
        json_file_name = "/db_settings.json"
        json_file_name = os.path.join(os.path.dirname(__file__) + json_file_name) # 解决相对路径文件的操作的问题
        #print json_file_name
        json_obj = JsonLoad(json_file_name)
        db_settings = json_obj.getdata()
        self.host = db_settings['MONGODB_HOST'] #主机名

        self.port = db_settings['MONGODB_PORT']  #端口

        self.db_name = db_settings['MONGODB_DBNAME']  #数据库名
        if collection_name is None:
            self.collection_name = db_settings['MONGODB_COLLECTION'] #集合名
        else:
            self.collection_name = collection_name
        self.collection_temp_name = db_settings['MONGODB_TEMP_COLLECTION']
        self.collection_negative_name = db_settings['MONGODB_COLLECTION_N']
        self.collection = None
        self.temp_collection = None
        self.collection_negative = None
        self.dbconnect()

    def dbConnection(self):
        if self.connection == None:
            #print "发生重连"
            self.dbconnect()
        return self.collection
    def dbConnectionTemp(self):

        if self.connection == None:
            self.dbconnect()
        return self.temp_collection
    def dbConnectionNegative(self):
        if self.connection == None:
            self.dbconnect()
        return self.collection_negative
 
    def dbconnect(self):
        try:
            
            self.connection = pymongo.MongoClient(
                self.host,
                self.port
                )
    
            db = self.connection[self.db_name]

            self.collection = db[self.collection_name]
            self.temp_collection = db[self.collection_temp_name]
            self.collection_negative = db[self.collection_negative_name]
            #return self.collection
        except BaseException,error:
            print error
            #self.collection = None
            self.dbclose()
    def dbClose(self):
        self.dbclose()

    def __del__(self):

        self.dbclose()

    def dbclose(self):

        try:
            if self.connection:
                self.connection.close()
                self.connection = None
                
        except BaseException,error:
            print error








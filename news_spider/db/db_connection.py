#coding=utf-8

import os
from scrapy.utils.project import get_project_settings
import pymongo

class DBConnection(object):

     def dbConnection(self):

        pass


class MongoDBConnection(DBConnection):

    def __init__(self,settings):

        #self.settings = get_project_settings()

        self.host = settings['MONGODB_HOST'] #主机名

        self.port = settings['MONGODB_PORT']  #端口

        self.db_name = settings['MONGODB_DBNAME']  #表名

        self.collection_name = settings['MONGODB_COLLECTION'] #集合名

    def dbConnection(self):



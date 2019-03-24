# -*- coding: utf-8 -*-

import pymongo
import os
import datetime
from bson import ObjectId
from db_connection import MongoDBConnection




class operation(object):

    def __init__(self,re_spider_log,collection_name = ""):
        self.filename = re_spider_log
        pass
    def db_close(self):
        pass
    def write_log(self,log):
        
        self.__touchfile()
        body = str(datetime.datetime.now()) + '操作数据库出错:' +str(log) + '\n'
        with open(self.filename,'a') as f:
            f.write(body)

    def __touchfile(self):
        
        if not os.path.exists(self.filename):
            file_dir = os.path.split(self.filename)[0]

            if not os.path.exists(file_dir):
                os.makedirs(file_dir)
            os.mknod(self.filename)  


# class user_operation(operation):

#     def __init__(self,re_spider_log,collection_name = ""):


#         self.obj = MongoDBConnection()
        
#         self.log_path = re_spider_log 

#     def verify_user(self,userInfo):

#         try:
#             connection = self.obj.dbConnection()
#             count = connection.find({"username":userInfo['username'],"password":userInfo["password"],"identity":userInfo["identity"]}).count()

#             if count == 1:
#                 return True
#             else:
#                 return False
#         except BaseException,error:
#             #logging.error(error)

#             return False
#         finally:
#             self.obj.dbClose()
class news_operation(operation):

    def __init__(self,re_spider_log,collection_name = ""):

        self.obj = MongoDBConnection()

        operation.__init__(self,re_spider_log)

        self.stop = False

    def reset_para(self):

        self.stop = False


    def search_news_page(self,condition,page_number = 10,page = 0,):

        try:
            if self.stop:
                return None
            self.collection_negative = self.obj.dbConnectionNegative()
            data = self.collection_negative.find(condition,{"_id":1,"article_url":1},no_cursor_timeout=True).hint([("article_publish_time",pymongo.ASCENDING)]).skip(page_number*page).limit(page_number)

            if data.count(True) < page_number:
                self.stop = True
            return data
        except BaseException,error:
            self.write_log(error)
            return None
        finally:
            self.obj.dbclose()

    def delete_batch(self,data):

        try:
            self.collection_negative = self.obj.dbConnectionNegative()
            for one_data in data:
                self.collection_negative.remove({"_id":one_data['_id']})
            return True
        except BaseException,error:
            self.write_log(error)
            return False
            
        finally:
            self.obj.dbclose()
    def update_db(self,one_data):
        
        #if  one_data['flag'] == 1 or one_data['flag'] == 2:

        return self.__update_all_content(one_data)
        #else:

        #return self.__update_only_article_content(one_data)

    def __update_all_content(self,one_data):
        
        try:
            #print "article_content:",one_data['article_content']
            #print "simhash",type(one_data['simhash'])
            self.collection_negative = self.obj.dbConnectionNegative()
            self.collection_negative.update({'_id':one_data['_id']},{"$set":{"article_content":one_data['article_content'],"processed_content":one_data['processed_content'],"simhash":str(one_data['simhash']),"is_repeate":0}})
            return True
        except BaseException,error:
            self.write_log(error)
            return False
            
        finally:
            self.obj.dbclose() 
    def __update_only_article_content(self,one_data):
        try:
            self.collection_negative = self.obj.dbConnectionNegative()
            self.collection_negative.update({'_id':one_data['_id']},{"$set":{"article_content":one_data['article_content'],"is_repeate":0}})
            return True
        except BaseException,error:
            self.write_log(error)
            return False
            
        finally:
            self.obj.dbclose() 


            

# if __name__ == "__main__":

#     commodity_operation_obj = commodity_operation()
     
#     if commodity_operation_obj.delete_commodity("58fe2c21e1382315154d4a30"):
#         print "58fe2c21e1382315154d4a30 success "

#     if commodity_operation_obj.delete_commodity("58fe2d1ee13823154b6cca62"):
#         print "58fe2d1ee13823154b6cca62 success"


#     if commodity_operation_obj.delete_commodity("58fe2d8ce138231578f44c61"):

#         print "58fe2d8ce138231578f44c61 success"
